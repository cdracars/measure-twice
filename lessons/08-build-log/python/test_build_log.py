import shutil
import tempfile
import unittest
from pathlib import Path

from build_log import (
    BadDate,
    EmptyText,
    LogEntry,
    MissingSeparator,
    append_entry,
    format_entry,
    load_log,
)

FIXTURES = Path(__file__).parent.parent / "fixtures"


def lines(entries: list[LogEntry]) -> list[str]:
    return [format_entry(entry) for entry in entries]


class LoadLogTest(unittest.TestCase):
    def test_loads_the_good_entries_in_order(self):
        self.assertEqual(
            [
                "2026-10-14: new 0.4 mm nozzle",
                "2026-10-16: replaced PTFE tube",
                "2026-10-18: note: PETG strings above 245 °C",
            ],
            lines(load_log(FIXTURES / "workshop.log").entries),
        )

    def test_reports_each_bad_line_with_its_line_number_and_error(self):
        problems = load_log(FIXTURES / "workshop.log").problems
        self.assertEqual([4, 6, 7], [p.line_number for p in problems])
        self.assertEqual(
            [MissingSeparator, BadDate, EmptyText],
            [type(p.error) for p in problems],
        )

    def test_an_empty_file_has_no_entries_and_no_problems(self):
        log = load_log(FIXTURES / "empty.log")
        self.assertEqual([], log.entries)
        self.assertEqual([], log.problems)

    def test_windows_line_endings_are_handled(self):
        entries = load_log(FIXTURES / "windows.log").entries
        self.assertEqual(["new nozzle", "dried PETG"], [e.text for e in entries])

    def test_a_missing_file_is_reported(self):
        with self.assertRaises(FileNotFoundError):
            load_log(FIXTURES / "no-such-file.log")


class AppendEntryTest(unittest.TestCase):
    """One example. Write the rest before the code."""

    def setUp(self):
        # A new, empty directory for each test, deleted afterwards.
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)

    def test_appending_to_a_new_file_creates_it(self):
        path = self.dir / "build.log"
        append_entry(path, LogEntry("2026-10-19", "levelled the bed"))
        self.assertEqual(["2026-10-19: levelled the bed"], lines(load_log(path).entries))

    def test_appending_twice_keeps_the_order(self):
        path = self.dir / "build.log"
        append_entry(path, LogEntry("2026-10-19", "levelled the bed"))
        append_entry(path, LogEntry("2026-10-20", "printed a calibration cube"))
        self.assertEqual(
            ["2026-10-19: levelled the bed", "2026-10-20: printed a calibration cube"],
            lines(load_log(path).entries),
        )

    def test_appending_to_an_existing_log_keeps_what_was_there(self):
        path = self.dir / "build.log"
        shutil.copy(FIXTURES / "workshop.log", path)
        append_entry(path, LogEntry("2026-10-19", "levelled the bed"))
        log = load_log(path)
        self.assertEqual(4, len(log.entries))
        self.assertEqual("2026-10-19: levelled the bed", format_entry(log.entries[-1]))
        self.assertEqual(3, len(log.problems))


if __name__ == "__main__":
    unittest.main()
