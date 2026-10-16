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
    entries: list[LogEntry] = []
    problems: list[Problem] = []
    # splitlines() handles "\n", "\r\n", and other line endings.
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            entries.append(parse_entry(line))
        except InvalidLogLine as error:
            problems.append(Problem(number, error))
    return LoadedLog(entries, problems)


def append_entry(path: Path, entry: LogEntry) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(format_entry(entry) + "\n")
