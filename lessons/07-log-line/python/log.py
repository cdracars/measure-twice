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
    # TODO: write the error tests in test_log.py first, then replace this line.
    raise NotImplementedError("TODO: implement parse_entry")


def format_entry(entry: LogEntry) -> str:
    """The line for an entry: "YYYY-MM-DD: text"."""
    # TODO: replace this line with your implementation.
    raise NotImplementedError("TODO: implement format_entry")


def truncate(text: str, max_chars: int) -> str:
    """The text if it has at most max_chars characters, otherwise its first
    max_chars characters followed by "…"."""
    raise NotImplementedError("TODO: implement truncate")
