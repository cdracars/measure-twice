import unittest

from log import LogEntry, format_entry, parse_entry, truncate


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


if __name__ == "__main__":
    unittest.main()
