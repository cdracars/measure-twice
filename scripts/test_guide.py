"""Tests for the guide. Run: python3 -m unittest discover -s scripts"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import guide
from guide import Exercise, Progress, TestResult

# Output captured from each test runner, trimmed. Paths are shortened to /r.

PHP_OUTPUT = """\
  ok    one metre of 1.75 mm PLA weighs about 3 g
  FAIL  zero length weighs nothing
        expected 0 (± 0.01), got 2.5

1 failed
"""

PYTHON_OUTPUT = """\
test_one_metre_of_pla_weighs_about_3_g (test_filament.FilamentMathTest.test_one_metre_of_pla_weighs_about_3_g) ... FAIL
test_a_1_kg_spool_holds_about_335_m (test_filament.FilamentMathTest.test_a_1_kg_spool_holds_about_335_m) ... ERROR
test_zero_length_weighs_nothing (test_filament.FilamentMathTest.test_zero_length_weighs_nothing) ... ok

======================================================================
ERROR: test_a_1_kg_spool_holds_about_335_m (test_filament.FilamentMathTest.test_a_1_kg_spool_holds_about_335_m)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/r/lessons/01-filament-math/python/test_filament.py", line 20, in test_a_1_kg_spool_holds_about_335_m
    self.assertAlmostEqual(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), delta=50.0)
  File "/r/lessons/01-filament-math/python/filament.py", line 9, in filament_length_mm
    raise NotImplementedError("TODO: implement filament_length_mm")
NotImplementedError: TODO: implement filament_length_mm

======================================================================
FAIL: test_one_metre_of_pla_weighs_about_3_g (test_filament.FilamentMathTest.test_one_metre_of_pla_weighs_about_3_g)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/r/lessons/01-filament-math/python/test_filament.py", line 8, in test_one_metre_of_pla_weighs_about_3_g
    self.assertAlmostEqual(2.98, filament_grams(1000.0, 1.75, 1.24), delta=0.01)
AssertionError: 2.98 != 2500.0 within 0.01 delta (2497.02 difference)

----------------------------------------------------------------------
Ran 3 tests in 0.001s
"""

TS_JUNIT = """\
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
\t<testsuite name="nozzleVerdict" tests="2" failures="1">
\t\t<testcase name="PLA in the middle of its range is ok" classname="test"/>
\t\t<testcase name="one metre of PLA weighs about 3 g" classname="test" failure="x">
\t\t\t<failure type="testCodeFailure" message="expected 2.98 (± 0.01), got 2.5">
AssertionError: expected 2.98 (± 0.01), got 2.5
    at assertClose (file:///r/lessons/01-filament-math/ts/filament.test.ts:7:10)
    at TestContext.&lt;anonymous&gt; (file:///r/lessons/01-filament-math/ts/filament.test.ts:14:3)
    at Test.runInAsyncScope (node:async_hooks:214:14)
</failure>
\t\t</testcase>
\t</testsuite>
\t<testcase name="top-level test" classname="test"/>
</testsuites>
"""

RUST_OUTPUT = """\
running 3 tests
test zero_length_weighs_nothing ... ok
test a_1_kg_spool_holds_about_335_m ... FAILED
test one_metre_of_pla_weighs_about_3_g ... FAILED

failures:

---- a_1_kg_spool_holds_about_335_m stdout ----

thread 'a_1_kg_spool_holds_about_335_m' (1197) panicked at lessons/01-filament-math/rust/src/lib.rs:14:5:
not yet implemented: implement filament_length_mm(1000, 1.75, 1.24)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

---- one_metre_of_pla_weighs_about_3_g stdout ----

thread 'one_metre_of_pla_weighs_about_3_g' (1198) panicked at lessons/01-filament-math/rust/tests/filament.rs:4:5:
expected 2.98 (± 0.01), got 2.5

failures:
    a_1_kg_spool_holds_about_335_m
    one_metre_of_pla_weighs_about_3_g

test result: FAILED. 1 passed; 2 failed; 0 ignored; 0 measured; 0 filtered out
"""


def by_name(results: list[TestResult]) -> dict[str, TestResult]:
    return {r.name: r for r in results}


class ParseTest(unittest.TestCase):
    def test_php(self):
        results = guide.parse_php(PHP_OUTPUT)
        self.assertEqual(
            [
                TestResult("one metre of 1.75 mm PLA weighs about 3 g", True),
                TestResult("zero length weighs nothing", False),
            ],
            results,
        )
        self.assertEqual("expected 0 (± 0.01), got 2.5", results[1].message)

    def test_python(self):
        results = guide.parse_python(PYTHON_OUTPUT)
        self.assertEqual(
            [
                TestResult("test_one_metre_of_pla_weighs_about_3_g", False),
                TestResult("test_a_1_kg_spool_holds_about_335_m", False),
                TestResult("test_zero_length_weighs_nothing", True),
            ],
            results,
        )
        failures = by_name(results)
        self.assertEqual(
            "AssertionError: 2.98 != 2500.0 within 0.01 delta (2497.02 difference)",
            failures["test_one_metre_of_pla_weighs_about_3_g"].message,
        )
        stub = failures["test_a_1_kg_spool_holds_about_335_m"]
        self.assertEqual("NotImplementedError: TODO: implement filament_length_mm", stub.message)
        self.assertEqual("/r/lessons/01-filament-math/python/test_filament.py:20", stub.location)

    def test_ts_junit_skips_suites_and_reads_failures(self):
        results = guide.parse_ts(TS_JUNIT)
        self.assertEqual(
            [
                TestResult("PLA in the middle of its range is ok", True),
                TestResult("one metre of PLA weighs about 3 g", False),
                TestResult("top-level test", True),
            ],
            results,
        )
        self.assertEqual("expected 2.98 (± 0.01), got 2.5", results[1].message)
        self.assertEqual("/r/lessons/01-filament-math/ts/filament.test.ts:14", results[1].location)

    def test_ts_junit_that_is_not_xml_gives_no_results(self):
        self.assertEqual([], guide.parse_ts("SyntaxError: something broke"))

    def test_rust(self):
        results = guide.parse_rust(RUST_OUTPUT)
        self.assertEqual(
            [
                TestResult("zero_length_weighs_nothing", True),
                TestResult("a_1_kg_spool_holds_about_335_m", False),
                TestResult("one_metre_of_pla_weighs_about_3_g", False),
            ],
            results,
        )
        failures = by_name(results)
        stub = failures["a_1_kg_spool_holds_about_335_m"]
        self.assertEqual(
            "not yet implemented: implement filament_length_mm(1000, 1.75, 1.24)", stub.message
        )
        self.assertEqual("lessons/01-filament-math/rust/src/lib.rs:14", stub.location)
        self.assertEqual(
            "expected 2.98 (± 0.01), got 2.5",
            failures["one_metre_of_pla_weighs_about_3_g"].message,
        )

    def test_rust_compile_error_gives_no_results(self):
        self.assertEqual([], guide.parse_rust("error[E0308]: mismatched types\n"))


class MatchTest(unittest.TestCase):
    def test_a_phrase_matches_names_in_every_language_style(self):
        for name in [
            "a 1 kg spool of 1.75 mm PLA holds about 335 m",
            "test_a_1_kg_spool_holds_about_335_m",
            "a_1_kg_spool_holds_about_335_m",
        ]:
            with self.subTest(name=name):
                self.assertTrue(guide.matches(name, "1 kg spool"))

    def test_matching_ignores_case(self):
        self.assertTrue(guide.matches("PLA does not need an Enclosure", "enclosure"))

    def test_a_phrase_that_is_not_there_does_not_match(self):
        self.assertFalse(guide.matches("zero length weighs nothing", "1 kg spool"))

    def test_readable_names_drop_underscores_and_the_test_prefix(self):
        self.assertEqual(
            "zero length weighs nothing", guide.readable("test_zero_length_weighs_nothing")
        )
        self.assertEqual("PLA at its minimum is ok", guide.readable("PLA at its minimum is ok"))


def exercise(**overrides) -> Exercise:
    fields = {
        "lesson": "01-filament-math",
        "number": 1,
        "title": "Weight from a length",
        "task": "Implement it.",
        "kind": "check",
        "tests": ("weighs about 3 g", "zero length"),
        "exclude": (),
        "min_tests": 1,
        "hints": ("one", "two", "three"),
        "checklist": (),
    }
    fields.update(overrides)
    return Exercise(**fields)


RESULTS = [
    TestResult("one metre of PLA weighs about 3 g", True),
    TestResult("zero length weighs nothing", True),
    TestResult("a 1 kg spool holds about 335 m", False),
    TestResult("ABS needs an enclosure", False),
]


class EvaluateTest(unittest.TestCase):
    def test_only_the_exercise_tests_count(self):
        evaluation = guide.evaluate(exercise(), RESULTS)
        self.assertEqual(2, len(evaluation.selected))
        self.assertTrue(evaluation.passed)

    def test_a_failing_selected_test_means_not_passed(self):
        evaluation = guide.evaluate(exercise(tests=("1 kg spool",)), RESULTS)
        self.assertFalse(evaluation.passed)

    def test_all_selects_every_test_except_excluded_ones(self):
        evaluation = guide.evaluate(exercise(tests="all", exclude=("enclosure",)), RESULTS)
        self.assertEqual(3, len(evaluation.selected))

    def test_no_matching_tests_is_not_a_pass(self):
        evaluation = guide.evaluate(exercise(tests=("nothing like this",)), RESULTS)
        self.assertFalse(evaluation.passed)

    def test_selected_tests_follow_the_steps_phrases_then_names(self):
        results = [
            TestResult("zero length b", True),
            TestResult("one metre weighs about 3 g", True),
            TestResult("zero length a", True),
        ]
        selected = guide.evaluate(exercise(), results).selected
        self.assertEqual(
            ["one metre weighs about 3 g", "zero length a", "zero length b"],
            [r.name for r in selected],
        )

    def test_too_few_tests_is_not_enough(self):
        evaluation = guide.evaluate(exercise(tests=("enclosure",), min_tests=3), RESULTS)
        self.assertFalse(evaluation.enough)


class CompleteTest(unittest.TestCase):
    passing = tuple(TestResult(f"needs enclosure {n}", True) for n in range(3))
    failing = tuple(TestResult(f"needs enclosure {n}", False) for n in range(3))

    def tests_first(self) -> Exercise:
        return exercise(kind="tests-first", tests=("enclosure",), min_tests=3)

    def test_a_check_exercise_is_complete_when_its_tests_pass(self):
        self.assertTrue(guide.is_complete(exercise(), guide.evaluate(exercise(), RESULTS), False))

    def test_tests_first_needs_to_have_seen_the_tests_fail(self):
        evaluation = guide.evaluate(self.tests_first(), list(self.passing))
        self.assertFalse(guide.is_complete(self.tests_first(), evaluation, seen_red=False))
        self.assertTrue(guide.is_complete(self.tests_first(), evaluation, seen_red=True))

    def test_red_counts_only_with_enough_tests(self):
        self.assertTrue(guide.counts_as_red(guide.evaluate(self.tests_first(), list(self.failing))))
        too_few = [TestResult("needs enclosure", False)]
        self.assertFalse(guide.counts_as_red(guide.evaluate(self.tests_first(), too_few)))

    def test_a_confirm_exercise_is_never_complete_on_its_own(self):
        confirm = exercise(kind="confirm", tests="all")
        evaluation = guide.evaluate(confirm, list(self.passing))
        self.assertFalse(guide.is_complete(confirm, evaluation, False))

    def test_a_read_exercise_is_never_complete_on_its_own(self):
        read = exercise(kind="read", tests="all")
        evaluation = guide.evaluate(read, list(self.passing))
        self.assertFalse(guide.is_complete(read, evaluation, False))


class HintTest(unittest.TestCase):
    def test_a_plain_hint_is_the_same_in_every_language(self):
        self.assertEqual("Think.", guide.hint_text("Think.", "rust"))

    def test_a_hint_table_picks_the_learners_language(self):
        hint = {"php": "Use M_PI.", "rust": "Use PI.", "default": "Use pi."}
        self.assertEqual("Use M_PI.", guide.hint_text(hint, "php"))
        self.assertEqual("Use pi.", guide.hint_text(hint, "python"))


class ScreenTest(unittest.TestCase):
    def test_progress_bar(self):
        self.assertEqual("████░░░░░░  40%", guide.progress_bar(2, 5, width=10))

    def test_progress_bar_with_nothing_to_do(self):
        self.assertEqual("░░░░░░░░░░   0%", guide.progress_bar(0, 0, width=10))

    def test_failures_show_name_message_and_location(self):
        failure = TestResult(
            "test_zero_length_weighs_nothing", False, "expected 0, got 2.5", "t.py:12"
        )
        text = guide.describe_result(failure)
        self.assertIn("zero length weighs nothing", text)
        self.assertIn("expected 0, got 2.5", text)
        self.assertIn("t.py:12", text)

    def test_a_passing_test_is_one_line(self):
        passing = TestResult("test_zero_length_weighs_nothing", True, "", "t.py:12")
        self.assertEqual(1, len(guide.describe_result(passing).splitlines()))
        self.assertIn("zero length weighs nothing", guide.describe_result(passing))

    def test_the_report_counts_and_lists_every_test_in_the_step(self):
        evaluation = guide.evaluate(exercise(), [*RESULTS, TestResult("zero length", False)])
        lines = guide.report(exercise(), evaluation, seen_red=False).splitlines()
        self.assertIn("2 of 3 passing", lines[0])
        self.assertIn("✓ one metre of PLA weighs about 3 g", lines[1])
        self.assertIn("✗ zero length", lines[2])
        self.assertIn("✓ zero length weighs nothing", lines[3])

    def test_a_test_stays_in_its_place_when_it_goes_green(self):
        def names(results):
            return [r.name for r in guide.evaluate(exercise(), results).selected]

        red = [TestResult("zero length weighs nothing", False), *RESULTS[:1]]
        green = [*RESULTS[:1], TestResult("zero length weighs nothing", True)]
        self.assertEqual(names(red), names(green))

    def test_paths_are_shown_relative_to_the_repository(self):
        self.assertEqual(
            "lessons/x/t.py:3", guide.relative(str(guide.ROOT / "lessons/x/t.py") + ":3")
        )
        self.assertEqual("elsewhere.py:3", guide.relative("elsewhere.py:3"))


class DoctorTest(unittest.TestCase):
    def test_version_numbers_are_found_in_tool_output(self):
        self.assertEqual((8, 3, 6), guide.version_in("PHP 8.3.6 (cli) (built: Sep  2 2026)"))
        self.assertEqual((22, 22, 0), guide.version_in("v22.22.0"))
        self.assertEqual((1, 97, 0), guide.version_in("cargo 1.97.0 (c980f4866 2026-06-30)"))
        self.assertIsNone(guide.version_in("command not found"))

    def test_a_new_enough_tool_has_no_problem(self):
        self.assertIsNone(guide.tool_problem("ts", "v22.22.0"))

    def test_an_old_tool_is_a_problem(self):
        problem = guide.tool_problem("ts", "v20.1.0")
        assert problem is not None
        self.assertIn("22.18", problem)
        self.assertIn("nodejs.org", problem)

    def test_a_missing_tool_is_a_problem(self):
        problem = guide.tool_problem("php", None)
        assert problem is not None
        self.assertIn("isn't installed", problem)


class ProgressTest(unittest.TestCase):
    exercises = (exercise(number=1), exercise(number=2))

    def test_steps_go_lesson_by_lesson_then_language_by_language(self):
        steps = guide.steps(list(self.exercises), ["php", "rust"])
        self.assertEqual(
            ["01.1:php", "01.2:php", "01.1:rust", "01.2:rust"],
            [guide.step_key(e, lang) for e, lang in steps],
        )

    def test_the_current_step_is_the_first_one_not_done(self):
        progress = Progress(languages=["php", "rust"], done={"01.1:php"})
        current = guide.current_step(list(self.exercises), progress)
        assert current is not None
        self.assertEqual("01.2:php", guide.step_key(*current))

    def test_no_current_step_when_everything_is_done(self):
        progress = Progress(languages=["php"], done={"01.1:php", "01.2:php"})
        self.assertIsNone(guide.current_step(list(self.exercises), progress))

    def test_progress_round_trips_through_a_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "progress.json"
            progress = Progress(languages=["ts"], done={"01.1:ts"}, hints={"01.2:ts": 2})
            progress.save(path)
            self.assertEqual(progress, Progress.load(path))

    def test_missing_progress_file_means_a_fresh_start(self):
        self.assertEqual(Progress(), Progress.load(Path("/no/such/progress.json")))

    def test_parse_languages_accepts_short_and_long_names(self):
        self.assertEqual(["php", "ts"], guide.parse_languages("PHP typescript"))
        self.assertEqual(["python", "rust"], guide.parse_languages("py, rust"))

    def test_parse_languages_rejects_unknown_names(self):
        with self.assertRaises(ValueError):
            guide.parse_languages("php cobol")


class LessonFilesTest(unittest.TestCase):
    """The real guide.toml files load and are well formed."""

    def test_every_guided_lesson_loads(self):
        exercises = guide.load_exercises(guide.ROOT)
        self.assertGreater(len(exercises), 0)
        for e in exercises:
            with self.subTest(exercise=e.key):
                self.assertIn(e.kind, ("check", "tests-first", "confirm", "read"))
                self.assertTrue(e.title and e.task and e.lesson_title and e.learned)
                self.assertTrue(e.lesson_intro, "a guided lesson says what it teaches and why")
                if e.kind in ("confirm", "read"):
                    self.assertTrue(e.checklist, "checklist steps have a checklist")
                else:
                    self.assertEqual(3, len(e.hints), "check exercises get three hints")
                for hint in e.hints:
                    for language in guide.LANGUAGES:
                        self.assertTrue(guide.hint_text(hint, language))


class ShowOnlyLanguagesTest(unittest.TestCase):
    """Hiding the lesson folders of languages not chosen, in .vscode/settings.json."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / ".vscode" / "settings.json"

    def excludes(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8")).get("files.exclude", {})

    def test_the_languages_not_chosen_are_hidden(self):
        message = guide.show_only_languages(self.path, ["php", "python"])
        self.assertEqual({"lessons/*/ts": True, "lessons/*/rust": True}, self.excludes())
        self.assertIn("PHP and Python", message or "")

    def test_choosing_a_language_again_shows_it(self):
        guide.show_only_languages(self.path, ["php"])
        guide.show_only_languages(self.path, ["php", "rust"])
        self.assertEqual({"lessons/*/python": True, "lessons/*/ts": True}, self.excludes())

    def test_other_settings_and_the_learners_own_choices_stay(self):
        self.path.parent.mkdir()
        self.path.write_text(
            json.dumps({"editor.tabSize": 2, "files.exclude": {"lessons/*/ts": False, "x": True}}),
            encoding="utf-8",
        )
        guide.show_only_languages(self.path, ["php"])
        settings = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(2, settings["editor.tabSize"])
        self.assertEqual(
            {"lessons/*/ts": False, "x": True, "lessons/*/python": True, "lessons/*/rust": True},
            settings["files.exclude"],
        )

    def test_three_languages_read_as_a_list(self):
        message = guide.show_only_languages(self.path, ["php", "python", "rust"])
        self.assertIn("PHP, Python and Rust", message or "")

    def test_choosing_all_four_later_shows_everything(self):
        guide.show_only_languages(self.path, ["php"])
        message = guide.show_only_languages(self.path, list(guide.LANGUAGES))
        self.assertEqual({}, self.excludes())
        self.assertIn("every language", message or "")

    def test_all_four_languages_need_no_settings_file(self):
        self.assertIsNone(guide.show_only_languages(self.path, list(guide.LANGUAGES)))
        self.assertFalse(self.path.exists())

    def test_nothing_changed_says_nothing(self):
        guide.show_only_languages(self.path, ["php"])
        self.assertIsNone(guide.show_only_languages(self.path, ["php"]))

    def test_a_settings_file_with_comments_is_left_alone(self):
        self.path.parent.mkdir()
        self.path.write_text('{\n  // mine\n  "editor.tabSize": 2\n}\n', encoding="utf-8")
        message = guide.show_only_languages(self.path, ["php"])
        self.assertIn("stay visible", message or "")
        self.assertIn("// mine", self.path.read_text(encoding="utf-8"))


PHP_FILES = {"php": {"edit": "php/filament.php", "tests": "php/test.php"}}
LESSON_01 = "lessons/01-filament-math"
IN_VSCODE = {"TERM_PROGRAM": "vscode"}


class OpenLessonFilesTest(unittest.TestCase):
    """Opening the lesson README and the file to edit in VS Code, with `code` mocked."""

    lesson_dir = guide.ROOT / "lessons" / "01-filament-math"

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.state_file = Path(temp.name) / "state.json"
        patches = [
            mock.patch.object(guide, "PROGRESS_FILE", Path(temp.name) / "progress.json"),
            mock.patch.object(guide, "STATE_FILE", self.state_file),
            mock.patch.object(guide, "ensure_ready", return_value=True),
            mock.patch.object(guide, "clear_screen"),
            mock.patch.object(guide, "wait_until_quiet", side_effect=lambda _l, _g, f: f),
            mock.patch.object(guide.shutil, "which", return_value="/usr/bin/code"),
            mock.patch.object(
                guide.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)
            ),
            mock.patch("builtins.print"),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        self.code = guide.subprocess.run

    def watch(self, keys, saves=1, open_files=True, env=None) -> int:
        """Run the watch loop on one failing step, with `saves` saves; returns the test runs."""
        mtimes = iter([{Path("f"): n} for n in range(saves)] + [{Path("f"): saves - 1}] * 99)
        with (
            mock.patch.dict(os.environ, env if env is not None else IN_VSCODE, clear=True),
            mock.patch.object(guide, "watched_files", side_effect=lambda _l, _g: next(mtimes)),
            mock.patch.object(
                guide, "run_tests", return_value=([TestResult("zero length", False)], "")
            ) as run_tests,
            mock.patch.object(guide, "read_key", side_effect=[*keys, "q"]),
        ):
            guide.watch([exercise(files=PHP_FILES)], Progress(languages=["php"]), open_files)
        return run_tests.call_count

    def code_calls(self) -> list[list[str]]:
        return [c.args[0] for c in self.code.call_args_list if c.args[0][0] == "code"]

    def test_a_step_opens_the_stub_and_tests_then_the_readme_so_the_readme_shows(self):
        self.watch([])
        stub, tests = self.lesson_dir / "php/filament.php", self.lesson_dir / "php/test.php"
        readme = self.lesson_dir / "README.md"
        self.assertEqual(
            [["code", "--reuse-window", str(stub), str(tests), str(readme)]], self.code_calls()
        )

    def test_saving_re_runs_the_tests_without_opening_the_files_again(self):
        self.assertEqual(3, self.watch([None, None], saves=3))
        self.assertEqual(1, len(self.code_calls()))

    def test_nothing_opens_outside_vscodes_terminal(self):
        self.watch([], env={})
        self.assertEqual([], self.code_calls())

    def test_guide_no_open_turns_it_off(self):
        self.watch([], env={**IN_VSCODE, "GUIDE_NO_OPEN": "1"})
        self.assertEqual([], self.code_calls())

    def test_guide_no_open_set_to_0_leaves_it_on(self):
        self.watch([], env={**IN_VSCODE, "GUIDE_NO_OPEN": "0"})
        self.assertEqual(1, len(self.code_calls()))

    def test_the_no_open_flag_turns_it_off(self):
        with mock.patch.object(guide, "watch", return_value=0) as watch:
            guide.main(["--no-open"])
        self.assertFalse(watch.call_args.args[2])

    def test_r_opens_the_lesson_readme_like_e_opens_the_file(self):
        with mock.patch.object(guide, "open_in_editor") as open_in_editor:
            self.watch(["r", "e"])
        self.assertEqual(
            [
                mock.call(self.lesson_dir / "README.md"),
                mock.call(self.lesson_dir / "php/filament.php"),
            ],
            open_in_editor.call_args_list,
        )

    def printed_by_watch(self, **kwargs) -> str:
        with mock.patch("builtins.print") as printed:
            self.watch([], **kwargs)
        return "\n".join(str(c.args[0]) for c in printed.call_args_list if c.args)

    def test_the_step_says_its_files_are_open_when_the_guide_opened_them(self):
        self.assertIn(guide.FILES_OPEN, self.printed_by_watch())

    def test_the_step_does_not_claim_files_are_open_outside_vscode(self):
        self.assertNotIn(guide.FILES_OPEN, self.printed_by_watch(env={}))

    def test_the_step_does_not_claim_files_are_open_when_code_fails(self):
        self.code.return_value = subprocess.CompletedProcess([], 1)
        self.assertNotIn(guide.FILES_OPEN, self.printed_by_watch())

    @unittest.skipUnless(os.name == "posix", "the running-guide check is POSIX only")
    def test_a_second_guide_refuses_to_start_while_one_is_running(self):
        alive = os.getppid()  # a process that's certainly running, and isn't this one
        self.state_file.write_text(json.dumps({"status": "ready", "pids": [alive]}))
        with mock.patch.object(guide, "watch_loop") as loop:
            self.assertEqual(1, guide.watch([], Progress(languages=["php"])))
        loop.assert_not_called()
        self.assertEqual("ready", json.loads(self.state_file.read_text())["status"])

    def test_a_stopped_guide_does_not_block_a_new_one(self):
        self.state_file.write_text(json.dumps({"status": "stopped", "pids": [os.getppid()]}))
        self.assertIsNone(guide.running_guide())

    def test_while_choosing_languages_the_panel_hears_the_guide_is_setting_up(self):
        published = []
        with (
            mock.patch.object(guide, "publish", side_effect=published.append),
            mock.patch.object(guide, "ensure_ready", return_value=False),
        ):
            guide.watch([], Progress())
        self.assertEqual(["setup", "stopped"], [s["status"] for s in published])

    def test_a_missing_toolchain_is_shown_in_the_panel(self):
        published = []
        with (
            mock.patch.object(guide, "publish", side_effect=published.append),
            mock.patch.object(guide, "ensure_ready", return_value=False),
            mock.patch.object(guide, "doctor", return_value=["Rust: cargo not found"]),
        ):
            guide.watch([], Progress(languages=["rust"]))
        self.assertEqual({"status": "problems"}, {"status": published[-1]["status"]})
        self.assertEqual(["Rust: cargo not found"], published[-1]["problems"])

    def test_started_by_the_panel_the_terminal_stays_brief(self):
        with mock.patch("builtins.print") as printed:
            self.watch([], env={**IN_VSCODE, "GUIDE_PANEL": "1"})
        text = "\n".join(str(c.args[0]) for c in printed.call_args_list if c.args)
        self.assertIn(guide.PANEL_NOTE, text)
        self.assertIn("1 failing", text)
        self.assertNotIn("Next:", text)

    def test_without_the_panel_the_terminal_shows_the_whole_step(self):
        with mock.patch("builtins.print") as printed:
            self.watch([])
        text = "\n".join(str(c.args[0]) for c in printed.call_args_list if c.args)
        self.assertIn("Next:", text)
        self.assertNotIn(guide.PANEL_NOTE, text)

    def test_quitting_tells_the_panel_the_guide_has_stopped(self):
        self.watch([])
        self.assertEqual("stopped", json.loads(self.state_file.read_text())["status"])

    def test_the_panel_sees_each_test_run(self):
        published = []
        with mock.patch.object(guide, "publish", side_effect=published.append):
            self.watch([])
        ready = [s for s in published if s["status"] == "ready"]
        self.assertEqual(1, len(ready))
        self.assertEqual(["zero length"], [f["name"] for f in ready[0]["results"]["failing"]])

    def test_a_hint_updates_the_panel(self):
        published = []
        with mock.patch.object(guide, "publish", side_effect=published.append):
            self.watch(["h"])
        ready = [s for s in published if s["status"] == "ready"]
        self.assertEqual([[], ["one"]], [s["hints"]["shown"] for s in ready])

    def test_a_code_command_that_fails_to_start_is_not_an_error(self):
        self.code.side_effect = OSError("no such file")
        self.assertFalse(guide.open_in_vscode([self.lesson_dir / "README.md"]))

    def test_a_lesson_without_files_opens_just_the_readme(self):
        self.assertEqual(
            [self.lesson_dir / "README.md"], guide.lesson_files(exercise(files={}), "php")
        )


class NextActionTest(unittest.TestCase):
    """Each step says what to do now; the very first one also says how the guide works."""

    def describe(self, step: Exercise, done=()) -> str:
        progress = Progress(languages=["php"], done=set(done))
        return guide.describe(step, "php", progress, [step])

    def test_a_check_step_says_which_file_to_change_and_that_saving_re_runs(self):
        self.assertEqual(
            f"Next: read the tests in {LESSON_01}/php/test.php, then write the code in"
            f" {LESSON_01}/php/filament.php and save. The tests re-run here.",
            guide.next_action(exercise(files=PHP_FILES), "php"),
        )

    def test_a_tests_first_step_says_to_write_the_tests_before_the_code(self):
        action = guide.next_action(exercise(kind="tests-first", files=PHP_FILES), "php")
        self.assertIn(f"write the tests in {LESSON_01}/php/test.php first", action)

    def test_a_step_that_needs_more_tests_says_to_add_one(self):
        action = guide.next_action(exercise(min_tests=7, files=PHP_FILES), "php")
        self.assertIn(f"add your test to {LESSON_01}/php/test.php", action)

    def test_a_read_step_says_to_open_the_tests_and_write_no_code(self):
        action = guide.next_action(exercise(kind="read", files=PHP_FILES), "php")
        self.assertIn(f"open {LESSON_01}/php/test.php", action)
        self.assertIn("No code yet", action)

    def test_files_named_from_the_repository_root_match_the_paths_listed_above(self):
        text = self.describe(exercise(files=PHP_FILES))
        self.assertIn(f"Tests  {LESSON_01}/php/test.php", text)
        self.assertIn(f"read the tests in {LESSON_01}/php/test.php", text)

    def test_the_open_files_note_shows_only_when_the_files_were_opened(self):
        progress = Progress(languages=["php"])
        step = exercise(files=PHP_FILES)
        self.assertIn(guide.FILES_OPEN, guide.describe(step, "php", progress, [step], True))
        self.assertNotIn(guide.FILES_OPEN, guide.describe(step, "php", progress, [step]))

    def test_a_read_step_can_be_confirmed_while_the_tests_still_fail(self):
        step, progress = exercise(kind="read", tests="all"), Progress(languages=["php"])
        failing = ([TestResult("a", False)], "")
        with (
            tempfile.TemporaryDirectory() as temp,
            mock.patch.object(guide, "PROGRESS_FILE", Path(temp) / "progress.json"),
            mock.patch.object(guide, "run_tests", return_value=failing),
            mock.patch.object(guide, "load_exercises", return_value=[step]),
            mock.patch("builtins.print"),
        ):
            guide.confirm(step, "php", progress)
        self.assertIn(guide.step_key(step, "php"), progress.done)

    def test_a_checklist_step_says_to_press_d(self):
        action = guide.next_action(exercise(kind="confirm", files=PHP_FILES), "php")
        self.assertIn("Press d when it's done", action)

    def test_every_step_shows_its_next_line(self):
        self.assertIn("Next: read the tests", self.describe(exercise(files=PHP_FILES)))

    def test_the_first_step_explains_how_the_guide_works(self):
        self.assertIn("How this works", self.describe(exercise(files=PHP_FILES)))

    def test_once_a_step_is_done_the_explanation_goes_away(self):
        text = self.describe(exercise(files=PHP_FILES), done=["01.1:php"])
        self.assertNotIn("How this works", text)

    def test_a_lesson_opens_with_what_it_teaches(self):
        step = exercise(files=PHP_FILES, lesson_intro="This lesson is about TDD.")
        self.assertIn("This lesson is about TDD.", self.describe(step))

    def test_the_lesson_intro_goes_away_once_a_step_of_that_lesson_is_done(self):
        step = exercise(number=2, files=PHP_FILES, lesson_intro="This lesson is about TDD.")
        self.assertNotIn("This lesson is about TDD.", self.describe(step, done=["01.1:php"]))

    def test_another_lessons_progress_does_not_hide_the_intro(self):
        step = exercise(files=PHP_FILES, lesson_intro="This lesson is about TDD.")
        self.assertIn("This lesson is about TDD.", self.describe(step, done=["00.1:php"]))


class PanelStateTest(unittest.TestCase):
    """What the guide tells the VS Code panel about the current step."""

    def state(self, step: Exercise, run=None, done=(), hints=0) -> dict:
        progress = Progress(languages=["php"], done=set(done))
        progress.hints[guide.step_key(step, "php")] = hints
        return guide.panel_state(step, "php", progress, [step], run, files_open=True)

    def run_with(self, step: Exercise, results: list[TestResult]) -> guide.Run:
        return guide.Run(False, "", "", guide.evaluate(step, results), False)

    def test_it_names_the_step_and_its_files_from_the_repository_root(self):
        state = self.state(exercise(files=PHP_FILES))
        self.assertEqual("Weight from a length", state["step"]["title"])
        self.assertEqual(f"{LESSON_01}/README.md", state["files"]["readme"])
        self.assertEqual(f"{LESSON_01}/php/test.php", state["files"]["tests"])
        self.assertEqual(f"{LESSON_01}/php/filament.php", state["files"]["edit"])
        self.assertTrue(state["step"]["next"].startswith("Next: read the tests"))

    def test_before_the_tests_run_it_says_testing(self):
        state = self.state(exercise(files=PHP_FILES))
        self.assertEqual("testing", state["status"])
        self.assertIsNone(state["results"])

    def test_it_lists_failures_without_terminal_colours(self):
        step = exercise(files=PHP_FILES)
        failing = TestResult("zero_length_weighs_nothing", False, "expected 0, got 2.5")
        state = self.state(step, self.run_with(step, [failing]))
        self.assertEqual("ready", state["status"])
        self.assertEqual(
            [{"name": "zero length weighs nothing", "message": "expected 0, got 2.5"}],
            state["results"]["failing"],
        )
        self.assertNotIn("\x1b", json.dumps(state))

    def test_a_read_step_says_its_failures_are_expected(self):
        step = exercise(kind="read", tests="all", files=PHP_FILES)
        state = self.state(step, self.run_with(step, [TestResult("a", False)]))
        self.assertEqual("quiet", state["results"]["tone"])
        self.assertIn("no code yet", state["results"]["notice"])

    def test_it_shows_only_the_hints_already_asked_for(self):
        state = self.state(exercise(files=PHP_FILES), hints=2)
        self.assertEqual({"shown": ["one", "two"], "total": 3}, state["hints"])

    def test_the_lesson_intro_and_how_this_works_go_once_a_step_is_done(self):
        step = exercise(files=PHP_FILES, lesson_intro="About TDD.")
        self.assertEqual("About TDD.", self.state(step)["step"]["intro"])
        later = self.state(step, done=["01.9:php"])["step"]
        self.assertIsNone(later["intro"])
        self.assertIsNone(later["how_this_works"])

    def test_it_lists_this_process_so_the_panel_can_find_the_terminal(self):
        self.assertIn(os.getppid(), self.state(exercise(files=PHP_FILES))["pids"])

    def test_publishing_writes_json_and_never_breaks_the_guide(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "state.json"
            with mock.patch.object(guide, "STATE_FILE", target):
                guide.publish({"status": "stopped"})
            self.assertEqual({"status": "stopped"}, json.loads(target.read_text()))
            with mock.patch.object(guide, "STATE_FILE", Path(temp) / "missing" / "state.json"):
                guide.publish({"status": "stopped"})


if __name__ == "__main__":
    unittest.main()
