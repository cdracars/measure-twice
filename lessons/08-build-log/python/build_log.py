import re
from dataclasses import dataclass
from pathlib import Path

# From lesson 07, finished.


@dataclass(frozen=True)
class LogEntry:
    date: str
    text: str


class InvalidLogLine(ValueError):
    pass


class MissingSeparator(InvalidLogLine):
    pass


class BadDate(InvalidLogLine):
    pass


class EmptyText(InvalidLogLine):
    pass


def parse_entry(line: str) -> LogEntry:
    date, separator, text = line.partition(":")
    if not separator:
        raise MissingSeparator(f"no ':' in {line!r}")
    date, text = date.strip(), text.strip()
    match = re.fullmatch(r"\d{4}-(\d{2})-(\d{2})", date)
    if match is None or not (1 <= int(match[1]) <= 12 and 1 <= int(match[2]) <= 31):
        raise BadDate(f"not a YYYY-MM-DD date: {date!r}")
    if not text:
        raise EmptyText(f"no text after the date in {line!r}")
    return LogEntry(date, text)


def format_entry(entry: LogEntry) -> str:
    return f"{entry.date}: {entry.text}"


# New in this lesson.


@dataclass(frozen=True)
class Problem:
    """One bad line in a log file."""

    line_number: int
    error: InvalidLogLine


@dataclass(frozen=True)
class LoadedLog:
    """Everything read from a log file: the good entries and the bad lines."""

    entries: list[LogEntry]
    problems: list[Problem]


def load_log(path: Path) -> LoadedLog:
    """Raises FileNotFoundError if the file doesn't exist."""
    # TODO: replace this line with your implementation.
    raise NotImplementedError("TODO: implement load_log")


def append_entry(path: Path, entry: LogEntry) -> None:
    # TODO: write the tests in test_build_log.py first, then replace this line.
    raise NotImplementedError("TODO: implement append_entry")
