"""The Measure Twice guide: walks you through the lessons one exercise at a time.

Usage: ./scripts/guide [command]

  (no command)   show your current exercise and re-run its tests every time
                 you save. Keys (then Enter): h hint · e edit · r read the
                 lesson README · o full output · d done (checklists) · q quit.
                 In VS Code's terminal (and Codespaces) each step opens the
                 lesson README and the file you edit; --no-open, or setting
                 GUIDE_NO_OPEN=1, turns that off.
  start [langs]  choose your languages, strongest first: start php python ts rust
  status         what you've done and what's next
  hint           show the next hint for the current exercise
  done           confirm the current checklist exercise
  check          run the current exercise's tests once
  doctor         check your toolchains are installed and new enough
  verify         (for course authors) check every guided exercise; add
                 --structure to only check that each exercise finds its tests

Exercises live in lessons/*/guide.toml. Your progress is kept in
.guide-progress.json, which git ignores. Works with any editor.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import tomllib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = ROOT / ".guide-progress.json"

LANGUAGES = ("php", "python", "ts", "rust")
LANGUAGE_NAMES = {"php": "PHP", "python": "Python", "ts": "TypeScript", "rust": "Rust"}
LANGUAGE_ALIASES = {
    "php": "php",
    "python": "python",
    "py": "python",
    "ts": "ts",
    "typescript": "ts",
    "rust": "rust",
    "rs": "rust",
}


# Test results, parsed from each language's test runner output.


@dataclass(frozen=True)
class TestResult:
    __test__ = False  # not a test case, despite the name

    name: str
    passed: bool
    message: str = field(default="", compare=False)
    location: str = field(default="", compare=False)


def parse_php(output: str) -> list[TestResult]:
    """Lines like '  ok    name' and '  FAIL  name', with the message indented below."""
    results = []
    lines = output.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^  (ok|FAIL) +(.+)$", line)
        if not match:
            continue
        message = ""
        if (
            match[1] == "FAIL"
            and index + 1 < len(lines)
            and lines[index + 1].startswith("        ")
        ):
            message = lines[index + 1].strip()
        results.append(TestResult(match[2].strip(), match[1] == "ok", message))
    return results


SEPARATOR = "-" * 70


def parse_python(output: str) -> list[TestResult]:
    """unittest -v: one 'name (...) ... ok' line per test, then a block per failure."""
    details: dict[str, tuple[str, str]] = {}
    for block in output.split("=" * 70)[1:]:
        header = re.match(r"\s*(?:FAIL|ERROR): (test\w*)", block)
        parts = block.split(SEPARATOR)
        if not header or len(parts) < 2 or header[1] in details:
            continue
        traceback = parts[1]
        lines = [line for line in traceback.splitlines() if line.strip()]
        message = lines[-1].strip() if lines else ""
        places = re.findall(r'File "([^"]*/[^"/]*test[^"/]*\.py)", line (\d+)', traceback)
        location = f"{places[-1][0]}:{places[-1][1]}" if places else ""
        details[header[1]] = (message, location)
    return [
        TestResult(m[1], m[2] == "ok", *details.get(m[1], ("", "")))
        for m in re.finditer(r"^(test\w*) \(.*\) \.\.\. (\w+)", output, re.MULTILINE)
    ]


def parse_ts(junit_xml: str) -> list[TestResult]:
    """JUnit XML from Node's test runner. Suites are skipped; only test cases count."""
    try:
        tree = ET.fromstring(junit_xml)
    except ET.ParseError:
        return []
    results = []
    for case in tree.iter("testcase"):
        failure = case.find("failure")
        if failure is None:
            results.append(TestResult(case.get("name", ""), True))
            continue
        text = failure.text or ""
        message = failure.get("message") or next(
            (line.strip() for line in text.splitlines() if line.strip()), ""
        )
        places = re.findall(r"file://(\S+?\.test\.ts):(\d+):\d+", text)
        location = f"{places[-1][0]}:{places[-1][1]}" if places else ""
        results.append(TestResult(case.get("name", ""), False, message, location))
    return results


def parse_rust(output: str) -> list[TestResult]:
    """cargo test: 'test name ... ok' lines, then a '---- name stdout ----' block per failure."""
    details: dict[str, tuple[str, str]] = {}
    blocks = re.finditer(
        r"^---- (\S+) stdout ----\n(.*?)(?=^---- |^failures:\s*$|\Z)",
        output,
        re.MULTILINE | re.DOTALL,
    )
    for block in blocks:
        panic = re.search(r"panicked at (.+?):(\d+):\d+:\n(.*)", block[2], re.DOTALL)
        if not panic:
            continue
        message_lines = []
        for line in panic[3].splitlines():
            if not line.strip() or line.startswith(("note:", "stack backtrace:")):
                break
            message_lines.append(line.strip())
        details[block[1]] = (" ".join(message_lines), f"{panic[1]}:{panic[2]}")
    return [
        TestResult(m[1], m[2] == "ok", *details.get(m[1], ("", "")))
        for m in re.finditer(r"^test (\S+) \.\.\. (\w+)", output, re.MULTILINE)
    ]


def normalize(name: str) -> str:
    """Lowercase, with _ and - as spaces, and Python's test_ prefix dropped."""
    text = re.sub(r"[_\-\s]+", " ", name.lower()).strip()
    return text.removeprefix("test ")


def readable(name: str) -> str:
    """A test name as a sentence: underscores become spaces, test_ goes."""
    text = re.sub(r"_+", " ", name).strip()
    return text.removeprefix("test ")


def matches(name: str, phrase: str) -> bool:
    return normalize(phrase) in normalize(name)


# Exercises, from lessons/*/guide.toml.

Hint = str | dict[str, str]


def hint_text(hint: Hint, language: str) -> str:
    """A hint may be one text for every language, or a table by language with a default."""
    if isinstance(hint, str):
        return hint.strip()
    return (hint.get(language) or hint.get("default", "")).strip()


@dataclass(frozen=True)
class Exercise:
    lesson: str
    number: int
    title: str
    task: str
    kind: str  # "check", "tests-first", or "confirm"
    tests: tuple[str, ...] | str  # phrases matched against test names, or "all"
    exclude: tuple[str, ...]
    min_tests: int
    hints: tuple[Hint, ...]
    checklist: tuple[str, ...]
    lesson_title: str = ""
    learned: str = ""
    files: dict[str, dict[str, str]] = field(default_factory=dict, compare=False)

    @property
    def key(self) -> str:
        return f"{self.lesson[:2]}.{self.number}"


def load_exercises(root: Path) -> list[Exercise]:
    exercises = []
    for path in sorted((root / "lessons").glob("*/guide.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        lesson = path.parent.name
        for number, item in enumerate(data["exercise"], start=1):
            tests = item.get("tests", "all")
            exercises.append(
                Exercise(
                    lesson=lesson,
                    number=number,
                    title=item["title"],
                    task=item["task"].strip(),
                    kind=item.get("kind", "check"),
                    tests=tests if tests == "all" else tuple(tests),
                    exclude=tuple(item.get("exclude", ())),
                    min_tests=item.get("min_tests", 1),
                    hints=tuple(item.get("hints", ())),
                    checklist=tuple(item.get("checklist", ())),
                    lesson_title=data.get("title", lesson),
                    learned=item.get("learned", ""),
                    files=data.get("files", {}),
                )
            )
    return exercises


def lesson_count(root: Path) -> int:
    return len([p for p in (root / "lessons").iterdir() if p.is_dir()])


@dataclass(frozen=True)
class Evaluation:
    selected: list[TestResult]
    passed: bool
    enough: bool


def evaluate(exercise: Exercise, results: list[TestResult]) -> Evaluation:
    def wanted(result: TestResult) -> bool:
        if any(matches(result.name, phrase) for phrase in exercise.exclude):
            return False
        if exercise.tests == "all":
            return True
        return any(matches(result.name, phrase) for phrase in exercise.tests)

    selected = [r for r in results if wanted(r)]
    passed = bool(selected) and all(r.passed for r in selected)
    return Evaluation(selected, passed, enough=len(selected) >= exercise.min_tests)


def counts_as_red(evaluation: Evaluation) -> bool:
    """Enough tests, and at least one failing: what writing tests first looks like."""
    return evaluation.enough and not evaluation.passed


def is_complete(exercise: Exercise, evaluation: Evaluation, seen_red: bool) -> bool:
    if exercise.kind == "confirm":
        return False  # the learner confirms it with `done`
    if not (evaluation.passed and evaluation.enough):
        return False
    return seen_red or exercise.kind != "tests-first"


# Progress through the course.


@dataclass
class Progress:
    languages: list[str] = field(default_factory=list)
    done: set[str] = field(default_factory=set)
    hints: dict[str, int] = field(default_factory=dict)
    seen_red: set[str] = field(default_factory=set)

    @classmethod
    def load(cls, path: Path) -> Progress:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return cls()
        return cls(
            languages=data.get("languages", []),
            done=set(data.get("done", [])),
            hints=data.get("hints", {}),
            seen_red=set(data.get("seen_red", [])),
        )

    def save(self, path: Path) -> None:
        data = {
            "languages": self.languages,
            "done": sorted(self.done),
            "hints": self.hints,
            "seen_red": sorted(self.seen_red),
        }
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


Step = tuple[Exercise, str]


def step_key(exercise: Exercise, language: str) -> str:
    return f"{exercise.key}:{language}"


def steps(exercises: list[Exercise], languages: list[str]) -> list[Step]:
    """Each lesson in every language before the next lesson, as the README suggests."""
    lessons = sorted({e.lesson for e in exercises})
    return [
        (e, lang)
        for lesson in lessons
        for lang in languages
        for e in exercises
        if e.lesson == lesson
    ]


def current_step(exercises: list[Exercise], progress: Progress) -> Step | None:
    for exercise, lang in steps(exercises, progress.languages):
        if step_key(exercise, lang) not in progress.done:
            return exercise, lang
    return None


def next_step_after(exercises: list[Exercise], progress: Progress, key: str) -> Step | None:
    all_steps = steps(exercises, progress.languages)
    keys = [step_key(*s) for s in all_steps]
    after = all_steps[keys.index(key) + 1 :] if key in keys else all_steps
    return next((s for s in after if step_key(*s) not in progress.done), None)


def parse_languages(text: str) -> list[str]:
    languages = []
    for word in re.split(r"[\s,]+", text.strip().lower()):
        if not word:
            continue
        if word not in LANGUAGE_ALIASES:
            raise ValueError(f"unknown language: {word} (use php, python, ts, rust)")
        languages.append(LANGUAGE_ALIASES[word])
    return list(dict.fromkeys(languages))


# Toolchains.

TOOLS = {
    "php": ("PHP", (8, 3), "https://www.php.net/downloads"),
    "python": ("Python", (3, 12), "https://www.python.org/downloads/"),
    "ts": ("Node.js", (22, 18), "https://nodejs.org/"),
    "rust": ("Rust", (1, 85), "https://rustup.rs/"),
}


def version_command(language: str) -> list[str]:
    return {
        "php": [os.environ.get("PHP", "php"), "--version"],
        "python": [sys.executable, "--version"],
        "ts": ["node", "--version"],
        "rust": ["cargo", "--version"],
    }[language]


def version_in(text: str) -> tuple[int, ...] | None:
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", text)
    return tuple(int(part) for part in match.groups()) if match else None


def tool_problem(language: str, version_output: str | None) -> str | None:
    """What's wrong with a language's toolchain, given its --version output (None: missing)."""
    name, minimum, link = TOOLS[language]
    wanted = ".".join(str(n) for n in minimum)
    if version_output is None:
        return f"{name} isn't installed. You need {wanted} or newer: {link}"
    version = version_in(version_output)
    if version is None or version[: len(minimum)] < minimum:
        found = ".".join(str(n) for n in version) if version else "an unknown version"
        return f"{name} {found} is too old. You need {wanted} or newer: {link}"
    return None


def doctor(languages: list[str]) -> list[str]:
    problems = []
    for language in languages:
        try:
            done = subprocess.run(
                version_command(language), capture_output=True, text=True, check=False
            )
            output: str | None = done.stdout + done.stderr
        except FileNotFoundError:
            output = None
        problem = tool_problem(language, output)
        if problem:
            problems.append(problem)
    return problems


# Running the tests.


def run_tests(lesson: str, language: str) -> tuple[list[TestResult], str]:
    """Run one lesson's tests in one language: (results, output to show the learner)."""
    lesson_dir = ROOT / "lessons" / lesson
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "RUST_BACKTRACE": "0"}

    def run(command: list[str], cwd: Path = ROOT) -> str:
        try:
            done = subprocess.run(
                command,
                cwd=cwd,
                env=env,
                capture_output=True,
                check=False,
                text=True,
                timeout=300,
            )
        except FileNotFoundError:
            return f"Couldn't run {command[0]}. Run ./scripts/guide doctor to check your setup.\n"
        except subprocess.TimeoutExpired:
            return "The tests took more than 5 minutes and were stopped.\n"
        return done.stdout + done.stderr

    if language == "php":
        output = run([os.environ.get("PHP", "php"), str(lesson_dir / "php" / "test.php")])
        return parse_php(output), output
    if language == "python":
        output = run([sys.executable, "-m", "unittest", "-v"], cwd=lesson_dir / "python")
        return parse_python(output), output
    if language == "rust":
        output = run(["cargo", "test", "--manifest-path", str(lesson_dir / "rust" / "Cargo.toml")])
        return parse_rust(output), output
    with tempfile.TemporaryDirectory() as temp:
        junit = Path(temp) / "junit.xml"
        test_files = sorted(str(p) for p in (lesson_dir / "ts").glob("*.test.ts"))
        output = run(
            [
                "node",
                "--test",
                "--test-reporter=spec",
                "--test-reporter-destination=stdout",
                "--test-reporter=junit",
                f"--test-reporter-destination={junit}",
                *test_files,
            ]
        )
        xml = junit.read_text(encoding="utf-8") if junit.exists() else ""
        return parse_ts(xml), output


# Showing things on screen.

COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def bold(text: str) -> str:
    return paint(text, "1")


def green(text: str) -> str:
    return paint(text, "32")


def red(text: str) -> str:
    return paint(text, "31")


def dim(text: str) -> str:
    return paint(text, "2")


def cyan(text: str) -> str:
    return paint(text, "36")


def clear_screen() -> None:
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")


def relative(path_and_line: str) -> str:
    """A path inside the repository, shown from the repository root (clickable in most terminals)."""
    prefix = str(ROOT) + os.sep
    return path_and_line.removeprefix(prefix)


def progress_bar(done: int, total: int, width: int = 20) -> str:
    fraction = done / total if total else 0
    filled = round(fraction * width)
    return "█" * filled + "░" * (width - filled) + f" {round(fraction * 100):3d}%"


def tail(text: str, lines: int = 60) -> str:
    kept = text.rstrip().splitlines()
    if len(kept) <= lines:
        return "\n".join(kept)
    return "\n".join([dim(f"... ({len(kept) - lines} earlier lines hidden)"), *kept[-lines:]])


def describe_failure(result: TestResult) -> str:
    lines = [f"  {red('✗')} {readable(result.name)}"]
    if result.message:
        lines.append(f"      {result.message}")
    if result.location:
        lines.append(dim(f"      at {relative(result.location)}"))
    return "\n".join(lines)


def header(exercise: Exercise, language: str, progress: Progress, exercises: list[Exercise]) -> str:
    all_steps = steps(exercises, progress.languages)
    done = sum(1 for s in all_steps if step_key(*s) in progress.done)
    in_lesson = [e for e in exercises if e.lesson == exercise.lesson]
    lesson_number = int(exercise.lesson[:2])
    return "\n".join(
        [
            bold(
                f"Lesson {lesson_number} of {lesson_count(ROOT)} · {exercise.lesson_title}"
                f" · {LANGUAGE_NAMES[language]}"
            ),
            dim(f"Guided so far {progress_bar(done, len(all_steps))}"),
            "",
            bold(f"Step {exercise.number} of {len(in_lesson)}: {exercise.title}"),
        ]
    )


def describe(
    exercise: Exercise, language: str, progress: Progress, exercises: list[Exercise]
) -> str:
    lines = [header(exercise, language, progress, exercises), "", exercise.task, ""]
    files = exercise.files.get(language, {})
    if files:
        lines.append(f"Read   lessons/{exercise.lesson}/README.md")
        lines.append(f"Edit   lessons/{exercise.lesson}/{files.get('edit', '')}")
        lines.append(f"Tests  lessons/{exercise.lesson}/{files.get('tests', '')}")
        lines.append("")
    if exercise.checklist:
        lines.append("Checklist:")
        lines.extend(f"  [ ] {item}" for item in exercise.checklist)
        lines.append("")
    shown = progress.hints.get(step_key(exercise, language), 0)
    for number, hint in enumerate(exercise.hints[:shown], start=1):
        lines.append(cyan(f"Hint {number}: {hint_text(hint, language)}"))
    if shown:
        lines.append("")
    return "\n".join(lines)


def report(exercise: Exercise, evaluation: Evaluation, seen_red: bool) -> str:
    if not evaluation.selected:
        return red("No tests for this step ran. The code may not compile: press o to see why.")
    passing = [r for r in evaluation.selected if r.passed]
    failing = [r for r in evaluation.selected if not r.passed]
    lines = [green(f"  ✓ {len(passing)} passing")] if passing else []
    lines.extend(describe_failure(r) for r in failing)
    if not evaluation.enough:
        lines.append(
            red(
                f"  Found {len(evaluation.selected)} test(s) for this step;"
                f" write at least {exercise.min_tests}."
            )
        )
    elif exercise.kind == "tests-first" and evaluation.passed and not seen_red:
        lines.append(
            red(
                "  These pass, but I never saw them fail. Break the code on purpose,"
                " save, watch the tests go red, then fix it."
            )
        )
    elif exercise.kind == "confirm" and evaluation.passed:
        lines.append(green("  Tests pass. Work through the checklist, then press d."))
    return "\n".join(lines)


def finished(exercise: Exercise, next_step: Step | None) -> str:
    lines = [green(bold(f"✓ Done: {exercise.title}"))]
    if exercise.learned:
        lines.append(f"  You practised: {exercise.learned}")
    if next_step:
        upcoming, language = next_step
        lines.append(dim(f"  Next up: {upcoming.title} ({LANGUAGE_NAMES[language]})"))
    return "\n".join(lines)


def all_done_message() -> str:
    return (
        green(bold("You've finished every guided step."))
        + "\nThe later lessons aren't guided yet: continue with their READMEs and"
        " ./scripts/check."
    )


# Commands.


@dataclass
class Run:
    complete: bool
    text: str
    output: str


def check_step(exercise: Exercise, language: str, progress: Progress) -> Run:
    """Run the tests for a step, record what happened, and say what it means."""
    results, output = run_tests(exercise.lesson, language)
    evaluation = evaluate(exercise, results)
    key = step_key(exercise, language)
    if counts_as_red(evaluation):
        progress.seen_red.add(key)
    complete = is_complete(exercise, evaluation, key in progress.seen_red)
    if complete:
        progress.done.add(key)
    progress.save(PROGRESS_FILE)
    return Run(complete, report(exercise, evaluation, key in progress.seen_red), output)


def ensure_ready(progress: Progress) -> bool:
    """Languages chosen and toolchains working, asking on the first run."""
    if not progress.languages:
        print(bold("Welcome to Measure Twice."))
        print("Which languages will you work in? List your strongest first.")
        print("For example: php python ts rust")
        try:
            answer = input("> ")
        except EOFError:
            answer = ""
        try:
            languages = parse_languages(answer)
        except ValueError as error:
            print(red(str(error)))
            return False
        if not languages:
            print("No languages chosen. Run ./scripts/guide start php python ts rust")
            return False
        progress.languages = languages
        progress.save(PROGRESS_FILE)
    problems = doctor(progress.languages)
    for problem in problems:
        print(red(problem))
    if problems:
        print("Fix these, then run ./scripts/guide again.")
    return not problems


def watched_files(lesson: str, language: str) -> dict[Path, float]:
    folder = ROOT / "lessons" / lesson / language
    return {
        path: path.stat().st_mtime
        for path in folder.rglob("*")
        if path.is_file() and not {"target", "__pycache__", "node_modules"} & set(path.parts)
    }


def wait_until_quiet(lesson: str, language: str, files: dict[Path, float]) -> dict[Path, float]:
    """Editors often save in bursts; wait until nothing has changed for a moment."""
    while True:
        time.sleep(0.3)
        latest = watched_files(lesson, language)
        if latest == files:
            return latest
        files = latest


def read_key(timeout: float) -> str | None:
    """A line typed by the learner, or None. Works where select() supports stdin."""
    try:
        import select

        ready, _, _ = select.select([sys.stdin], [], [], timeout)
    except (OSError, ValueError, ImportError):
        time.sleep(timeout)
        return None
    if not ready:
        return None
    line = sys.stdin.readline()
    return line.strip().lower()[:1] if line else "q"


def open_in_editor(path: Path) -> None:
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    command = editor.split() if editor else (["code"] if shutil.which("code") else None)
    if command is None:
        print(f"Open this file in your editor: {relative(str(path))}")
        print(dim("(Set EDITOR, or install VS Code's `code` command, to open it with e.)"))
        return
    subprocess.run([*command, str(path)], check=False)


def lesson_files(exercise: Exercise, language: str) -> list[Path]:
    """The lesson README, then the file the learner edits, if the lesson names one."""
    lesson_dir = ROOT / "lessons" / exercise.lesson
    edit = exercise.files.get(language, {}).get("edit")
    return [lesson_dir / "README.md", *([lesson_dir / edit] if edit else [])]


def can_open_in_vscode() -> bool:
    """Inside VS Code's own terminal, where `code` opens files in the same window."""
    if os.environ.get("GUIDE_NO_OPEN", "") not in ("", "0"):
        return False
    return os.environ.get("TERM_PROGRAM") == "vscode" and shutil.which("code") is not None


def open_in_vscode(paths: list[Path]) -> bool:
    """Open files in the VS Code window this terminal belongs to; False if that didn't work."""
    try:
        done = subprocess.run(
            ["code", "--reuse-window", *(str(p) for p in paths)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return done.returncode == 0


def watch(exercises: list[Exercise], progress: Progress, open_files: bool = True) -> int:
    if not ensure_ready(progress):
        return 1
    files: dict[Path, float] = {}
    shown: str | None = None
    last = Run(False, "", "")
    opened: str | None = None
    keys = "h hint · e edit · r README · o full output · d done · q quit  (then Enter)"
    while True:
        step = current_step(exercises, progress)
        if step is None:
            print(all_done_message())
            return 0
        exercise, language = step
        latest = watched_files(exercise.lesson, language)
        if latest != files or step_key(*step) != shown:
            if shown == step_key(*step):
                latest = wait_until_quiet(exercise.lesson, language, latest)
            files, shown = latest, step_key(*step)
            if open_files and opened != shown and can_open_in_vscode():
                open_in_vscode(lesson_files(exercise, language))
            opened = shown
            clear_screen()
            print(describe(exercise, language, progress, exercises))
            print(dim("Running the tests..."))
            last = check_step(exercise, language, progress)
            clear_screen()
            print(describe(exercise, language, progress, exercises))
            print(last.text)
            if last.complete:
                print("\n" + finished(exercise, current_step(exercises, progress)))
                time.sleep(2.5)
                continue
            print("\n" + dim(f"Save a file to re-run · {keys}"))
        key = read_key(0.5)
        if key == "q":
            return 0
        if key == "h":
            show_hint(exercise, language, progress)
        elif key == "e":
            edit = exercise.files.get(language, {}).get("edit")
            if edit:
                open_in_editor(ROOT / "lessons" / exercise.lesson / edit)
        elif key == "r":
            open_in_editor(ROOT / "lessons" / exercise.lesson / "README.md")
        elif key == "o":
            print(tail(last.output))
        elif key == "d":
            confirm(exercise, language, progress)
            shown = None


def show_hint(exercise: Exercise, language: str, progress: Progress) -> None:
    key = step_key(exercise, language)
    shown = progress.hints.get(key, 0)
    if shown >= len(exercise.hints):
        print("No more hints. The lesson README and the solutions branch are next.")
        return
    progress.hints[key] = shown + 1
    progress.save(PROGRESS_FILE)
    text = hint_text(exercise.hints[shown], language)
    print(cyan(f"Hint {shown + 1} of {len(exercise.hints)}: {text}"))


def confirm(exercise: Exercise, language: str, progress: Progress) -> None:
    if exercise.kind != "confirm":
        print("This step finishes by itself when its tests pass.")
        return
    results, _ = run_tests(exercise.lesson, language)
    if not evaluate(exercise, results).passed:
        print(red("Get the tests passing first, then confirm."))
        return
    progress.done.add(step_key(exercise, language))
    progress.save(PROGRESS_FILE)
    print(finished(exercise, current_step(load_exercises(ROOT), progress)))


def status(exercises: list[Exercise], progress: Progress) -> None:
    if not progress.languages:
        print("Not started yet. Run ./scripts/guide")
        return
    all_steps = steps(exercises, progress.languages)
    done = sum(1 for s in all_steps if step_key(*s) in progress.done)
    print(bold(f"Guided so far {progress_bar(done, len(all_steps))}"))
    current = current_step(exercises, progress)
    heading = None
    for exercise, language in all_steps:
        title = f"Lesson {int(exercise.lesson[:2])} · {exercise.lesson_title} · {LANGUAGE_NAMES[language]}"
        if title != heading:
            print("\n" + title)
            heading = title
        key = step_key(exercise, language)
        if key in progress.done:
            mark = green("✓")
        elif current and key == step_key(*current):
            mark = bold("→")
        else:
            mark = dim("·")
        print(f"  {mark} {exercise.title}")


def verify(exercises: list[Exercise], structure_only: bool) -> int:
    """For course authors: every exercise finds its tests, and (on solutions) passes."""
    problems = []
    cache: dict[tuple[str, str], list[TestResult]] = {}
    for exercise in exercises:
        for language in LANGUAGES:
            if language not in exercise.files:
                continue
            if (exercise.lesson, language) not in cache:
                cache[exercise.lesson, language] = run_tests(exercise.lesson, language)[0]
            results = cache[exercise.lesson, language]
            where = f"{exercise.key} {exercise.title} [{language}]"
            if exercise.tests != "all":
                for phrase in exercise.tests:
                    if not any(matches(r.name, phrase) for r in results):
                        problems.append(f"{where}: no test matches {phrase!r}")
            evaluation = evaluate(exercise, results)
            if not structure_only and not (evaluation.passed and evaluation.enough):
                count = len(evaluation.selected)
                problems.append(f"{where}: tests don't pass, or too few ({count})")
    for problem in problems:
        print(red(problem))
    print(f"{len(exercises)} exercises checked, {len(problems)} problem(s)")
    return 1 if problems else 0


def main(argv: list[str]) -> int:
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped into head
    exercises = load_exercises(ROOT)
    progress = Progress.load(PROGRESS_FILE)
    open_files = "--no-open" not in argv
    argv = [arg for arg in argv if arg != "--no-open"]
    command, args = (argv[0], argv[1:]) if argv else ("watch", [])

    if command in ("help", "-h", "--help"):
        print(__doc__)
        return 0
    if command == "verify":
        return verify(exercises, structure_only="--structure" in args)
    if command == "doctor":
        languages = progress.languages or list(LANGUAGES)
        problems = doctor(languages)
        for problem in problems:
            print(red(problem))
        if not problems:
            names = ", ".join(LANGUAGE_NAMES[lang] for lang in languages)
            print(green(f"All set: {names}."))
        return 1 if problems else 0
    if command == "start":
        try:
            languages = parse_languages(" ".join(args))
        except ValueError as error:
            print(red(str(error)))
            return 2
        if not languages:
            print("Name your languages, strongest first: ./scripts/guide start php python ts rust")
            return 2
        progress.languages = languages
        progress.save(PROGRESS_FILE)
        print(f"Languages: {', '.join(LANGUAGE_NAMES[lang] for lang in languages)}")
        print("Now run ./scripts/guide")
        return 0
    if command == "watch":
        try:
            return watch(exercises, progress, open_files)
        except KeyboardInterrupt:
            return 0
    if command == "status":
        status(exercises, progress)
        return 0

    if not ensure_ready(progress):
        return 1
    step = current_step(exercises, progress)
    if step is None:
        print(all_done_message())
        return 0
    exercise, language = step
    if command == "hint":
        show_hint(exercise, language, progress)
        return 0
    if command == "done":
        confirm(exercise, language, progress)
        return 0
    if command == "check":
        print(describe(exercise, language, progress, exercises))
        run = check_step(exercise, language, progress)
        print(run.text)
        if run.complete:
            print("\n" + finished(exercise, current_step(exercises, progress)))
        return 0 if run.complete else 1

    print(f"Unknown command: {command}\n")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
