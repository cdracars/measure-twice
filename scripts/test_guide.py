"""Tests for the guide. Run: python3 -m unittest discover -s scripts"""

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
        text = guide.describe_failure(failure)
        self.assertIn("zero length weighs nothing", text)
        self.assertIn("expected 0, got 2.5", text)
        self.assertIn("t.py:12", text)

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
                self.assertIn(e.kind, ("check", "tests-first", "confirm"))
                self.assertTrue(e.title and e.task and e.lesson_title and e.learned)
                self.assertTrue(e.lesson_intro, "a guided lesson says what it teaches and why")
                if e.kind != "confirm":
                    self.assertEqual(3, len(e.hints), "check exercises get three hints")
                for hint in e.hints:
                    for language in guide.LANGUAGES:
                        self.assertTrue(guide.hint_text(hint, language))


PHP_FILES = {"php": {"edit": "php/filament.php", "tests": "php/test.php"}}
IN_VSCODE = {"TERM_PROGRAM": "vscode"}


class OpenLessonFilesTest(unittest.TestCase):
    """Opening the lesson README and the file to edit in VS Code, with `code` mocked."""

    lesson_dir = guide.ROOT / "lessons" / "01-filament-math"

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        patches = [
            mock.patch.object(guide, "PROGRESS_FILE", Path(temp.name) / "progress.json"),
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
            "Next: read the tests in php/test.php, then write the code in php/filament.php"
            " and save. The tests re-run here.",
            guide.next_action(exercise(files=PHP_FILES), "php"),
        )

    def test_a_tests_first_step_says_to_write_the_tests_before_the_code(self):
        action = guide.next_action(exercise(kind="tests-first", files=PHP_FILES), "php")
        self.assertIn("write the tests in php/test.php first", action)

    def test_a_step_that_needs_more_tests_says_to_add_one(self):
        action = guide.next_action(exercise(min_tests=7, files=PHP_FILES), "php")
        self.assertIn("add your test to php/test.php", action)

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


if __name__ == "__main__":
    unittest.main()
