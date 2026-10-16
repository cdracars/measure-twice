import unittest

from log import (
    BadDate,
    EmptyText,
    LogEntry,
    MissingSeparator,
    format_entry,
    parse_entry,
    truncate,
)


class TruncateTest(unittest.TestCase):
    def test_short_text_is_unchanged(self):
        self.assertEqual("benchy", truncate("benchy", 10))

    def test_text_exactly_at_the_limit_is_unchanged(self):
        self.assertEqual("1234567890", truncate("1234567890", 10))

    def test_long_text_is_cut_and_marked(self):
        self.assertEqual("replaced…", truncate("replaced the nozzle", 8))

    def test_a_degree_sign_counts_as_one_character(self):
        self.assertEqual("nozzle at 215 °…", truncate("nozzle at 215 °C", 15))

    def test_an_emoji_counts_as_one_character(self):
        self.assertEqual("new spool 🧵…", truncate("new spool 🧵 loaded", 11))


class FormatEntryTest(unittest.TestCase):
    def test_format_an_entry(self):
        entry = LogEntry("2026-10-16", "replaced nozzle")
        self.assertEqual("2026-10-16: replaced nozzle", format_entry(entry))


class ParseEntryTest(unittest.TestCase):
    """Two examples. Write the error tests before the code."""

    def test_parse_a_simple_line(self):
        self.assertEqual(
            LogEntry("2026-10-16", "replaced nozzle"),
            parse_entry("2026-10-16: replaced nozzle"),
        )

    def test_parse_ignores_surrounding_spaces(self):
        self.assertEqual(
            LogEntry("2026-10-17", "raised Z offset"),
            parse_entry("  2026-10-17 :   raised Z offset  "),
        )

    def test_a_colon_inside_the_text_is_kept(self):
        self.assertEqual("note: PETG strings", parse_entry("2026-10-18: note: PETG strings").text)

    def test_format_undoes_parse(self):
        line = "2026-10-18: note: PETG strings above 245 °C"
        self.assertEqual(line, format_entry(parse_entry(line)))

    def test_a_line_without_a_colon_is_missing_its_separator(self):
        with self.assertRaises(MissingSeparator):
            parse_entry("2026-10-16 replaced nozzle")

    def test_bad_dates(self):
        for date in [
            "16/10/2026",
            "2026-13-01",
            "2026-00-10",
            "2026-10-32",
            "2026-10-00",
            "2026-1-5",
            "",
        ]:
            with self.subTest(date=date), self.assertRaises(BadDate):
                parse_entry(f"{date}: replaced nozzle")

    def test_blank_text_is_empty(self):
        with self.assertRaises(EmptyText):
            parse_entry("2026-10-16:   ")


if __name__ == "__main__":
    unittest.main()
