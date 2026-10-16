import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LogEntry:
    date: str
    text: str


# The errors. They're given: your job is to raise them.


class InvalidLogLine(ValueError):
    """Base class for every way a log line can be invalid."""


class MissingSeparator(InvalidLogLine):
    pass


class BadDate(InvalidLogLine):
    pass


class EmptyText(InvalidLogLine):
    pass


def parse_entry(line: str) -> LogEntry:
    """A log entry from a line like "2026-10-16: replaced nozzle".

    Raises an InvalidLogLine subclass if the line isn't valid.
    """
    date, separator, text = line.partition(":")
    if not separator:
        raise MissingSeparator(f"no ':' in {line!r}")

    date, text = date.strip(), text.strip()
    if not _is_valid_date(date):
        raise BadDate(f"not a YYYY-MM-DD date: {date!r}")
    if not text:
        raise EmptyText(f"no text after the date in {line!r}")
    return LogEntry(date, text)


def _is_valid_date(date: str) -> bool:
    """Whether a string looks like YYYY-MM-DD. Checks the shape, not the calendar."""
    match = re.fullmatch(r"\d{4}-(\d{2})-(\d{2})", date)
    if match is None:
        return False
    month, day = int(match[1]), int(match[2])
    return 1 <= month <= 12 and 1 <= day <= 31


def format_entry(entry: LogEntry) -> str:
    """The line for an entry: "YYYY-MM-DD: text"."""
    return f"{entry.date}: {entry.text}"


def truncate(text: str, max_chars: int) -> str:
    """The text if it has at most max_chars characters, otherwise its first
    max_chars characters followed by "…"."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "…"
