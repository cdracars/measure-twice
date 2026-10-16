import unittest
from pathlib import Path

from cli import USAGE, Output, run


class HelpAndErrorsTest(unittest.TestCase):
    def test_help_prints_the_usage(self):
        self.assertEqual(Output(0, stdout=USAGE), run(["help"]))

    def test_no_arguments_prints_the_usage_as_an_error(self):
        self.assertEqual(Output(2, stderr=USAGE), run([]))

    def test_an_unknown_command_is_an_error(self):
        self.assertEqual(
            Output(
                2, stderr="jig: unknown command: frobnicate\nrun 'jig help' to see the commands\n"
            ),
            run(["frobnicate"]),
        )


class GramsTest(unittest.TestCase):
    def test_grams_of_pla(self):
        self.assertEqual(Output(0, stdout="2.98 g\n"), run(["grams", "1000", "PLA"]))

    def test_accepts_a_lowercase_material(self):
        self.assertEqual(Output(0, stdout="12.83 g\n"), run(["grams", "4200", "petg"]))

    def test_rejects_a_bad_length(self):
        self.assertEqual(Output(2, stderr="jig: not a length: abc\n"), run(["grams", "abc", "PLA"]))

    def test_rejects_an_unknown_material(self):
        self.assertEqual(
            Output(2, stderr="jig: unknown material: Nylon\n"), run(["grams", "1000", "Nylon"])
        )

    def test_needs_exactly_two_arguments(self):
        self.assertEqual(
            Output(2, stderr="jig: usage: jig grams <length-mm> <material>\n"),
            run(["grams", "1000"]),
        )


class CheckTest(unittest.TestCase):
    def test_a_good_temperature(self):
        self.assertEqual(
            Output(0, stdout="ok: PLA prints at 190–220 °C\n"), run(["check", "PLA", "205"])
        )

    def test_a_cold_temperature(self):
        self.assertEqual(
            Output(1, stdout="too cold: PETG prints at 220–250 °C\n"), run(["check", "petg", "200"])
        )

    def test_a_hot_temperature(self):
        self.assertEqual(
            Output(1, stdout="too hot: TPU prints at 210–230 °C\n"), run(["check", "TPU", "240"])
        )

    def test_rejects_a_bad_temperature(self):
        self.assertEqual(
            Output(2, stderr="jig: not a temperature: hot\n"), run(["check", "PLA", "hot"])
        )

    def test_needs_exactly_two_arguments(self):
        self.assertEqual(
            Output(2, stderr="jig: usage: jig check <material> <nozzle-c>\n"),
            run(["check", "PLA", "205", "extra"]),
        )


class LogTest(unittest.TestCase):
    """No tests yet. Write them before the code."""

    FIXTURES = Path(__file__).parent.parent.parent / "08-build-log" / "fixtures"

    def test_summarizes_a_log_with_problems(self):
        self.assertEqual(
            Output(
                1,
                stdout="entries: 3\nproblems: 3\n  line 4: missing separator\n  line 6: bad date\n  line 7: empty text\n",
            ),
            run(["log", str(self.FIXTURES / "workshop.log")]),
        )

    def test_a_clean_log_succeeds(self):
        self.assertEqual(
            Output(0, stdout="entries: 2\nproblems: 0\n"),
            run(["log", str(self.FIXTURES / "windows.log")]),
        )

    def test_an_empty_file(self):
        self.assertEqual(
            Output(0, stdout="entries: 0\nproblems: 0\n"),
            run(["log", str(self.FIXTURES / "empty.log")]),
        )

    def test_a_missing_file_is_an_error(self):
        path = str(self.FIXTURES / "no-such-file.log")
        self.assertEqual(Output(2, stderr=f"jig: no such file: {path}\n"), run(["log", path]))

    def test_needs_exactly_one_argument(self):
        self.assertEqual(Output(2, stderr="jig: usage: jig log <file>\n"), run(["log"]))


if __name__ == "__main__":
    unittest.main()
