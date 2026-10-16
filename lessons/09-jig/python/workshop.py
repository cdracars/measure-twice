"""Finished pieces from lessons 01–08. You don't need to change this file."""

import math
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Material(Enum):
    PLA = "PLA"
    PETG = "PETG"
    ABS = "ABS"
    TPU = "TPU"

    def density(self) -> float:
        return {"PLA": 1.24, "PETG": 1.27, "ABS": 1.04, "TPU": 1.21}[self.value]

    def nozzle_range(self) -> tuple[int, int]:
        return {
            "PLA": (190, 220),
            "PETG": (220, 250),
            "ABS": (230, 260),
            "TPU": (210, 230),
        }[self.value]


class Verdict(Enum):
    TOO_COLD = "too cold"
    OK = "ok"
    TOO_HOT = "too hot"


def parse_material(text: str) -> Material | None:
    """The material, or None if the text isn't one. Ignores case and spaces."""
    try:
        return Material(text.strip().upper())
    except ValueError:
        return None


def parse_length_mm(text: str) -> float | None:
    """A length in mm such as "1000" or "12.5", or None if the text isn't one."""
    text = text.strip()
    return float(text) if re.fullmatch(r"\d+(\.\d+)?", text) else None


def parse_celsius(text: str) -> int | None:
    """A whole number of °C such as "205", or None if the text isn't one."""
    text = text.strip()
    return int(text) if re.fullmatch(r"-?\d+", text) else None


def filament_grams(length_mm: float, material: Material) -> float:
    """Weight in grams of a length of 1.75 mm filament."""
    area_mm2 = math.pi * (1.75 / 2) ** 2
    return length_mm * area_mm2 / 1000 * material.density()


def nozzle_verdict(material: Material, nozzle_c: int) -> Verdict:
    low, high = material.nozzle_range()
    if nozzle_c < low:
        return Verdict.TOO_COLD
    if nozzle_c > high:
        return Verdict.TOO_HOT
    return Verdict.OK


# The Build Log, from lessons 07 and 08.


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


@dataclass(frozen=True)
class Problem:
    line_number: int
    error: InvalidLogLine


@dataclass(frozen=True)
class LoadedLog:
    entries: list[LogEntry]
    problems: list[Problem]


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


def load_log(path: Path) -> LoadedLog:
    """Raises FileNotFoundError if the file doesn't exist."""
    entries: list[LogEntry] = []
    problems: list[Problem] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            entries.append(parse_entry(line))
        except InvalidLogLine as error:
            problems.append(Problem(number, error))
    return LoadedLog(entries, problems)
