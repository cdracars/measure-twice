from dataclasses import dataclass
from pathlib import Path

from workshop import (
    BadDate,
    MissingSeparator,
    Verdict,
    filament_grams,
    load_log,
    nozzle_verdict,
    parse_celsius,
    parse_length_mm,
    parse_material,
)

USAGE = """\
usage: jig <command> [arguments]

commands:
  grams <length-mm> <material>   weight of 1.75 mm filament
  check <material> <nozzle-c>    is this nozzle temperature right?
  log <file>                     summarize a Build Log
  help                           show this message
"""


@dataclass(frozen=True)
class Output:
    """What running jig produced: an exit code and the text for each stream."""

    code: int
    stdout: str = ""
    stderr: str = ""


def run(args: list[str]) -> Output:
    """Run jig with the given arguments (not including the program name).

    Never prints and never exits: it returns what should happen.
    """
    match args:
        case []:
            return Output(2, stderr=USAGE)
        case ["help", *_]:
            return Output(0, stdout=USAGE)
        case ["grams", length, material]:
            return grams_command(length, material)
        case ["grams", *_]:
            return error("usage: jig grams <length-mm> <material>")
        case ["check", material, nozzle]:
            return check_command(material, nozzle)
        case ["check", *_]:
            return error("usage: jig check <material> <nozzle-c>")
        case ["log", path]:
            return log_command(Path(path))
        case ["log", *_]:
            return error("usage: jig log <file>")
        case [command, *_]:
            return error(f"unknown command: {command}\nrun 'jig help' to see the commands")
    raise AssertionError("unreachable")  # every list matches a case above


def error(message: str) -> Output:
    return Output(2, stderr=f"jig: {message}\n")


def grams_command(length_text: str, material_text: str) -> Output:
    length = parse_length_mm(length_text)
    if length is None:
        return error(f"not a length: {length_text}")
    material = parse_material(material_text)
    if material is None:
        return error(f"unknown material: {material_text}")
    return Output(0, stdout=f"{filament_grams(length, material):.2f} g\n")


def check_command(material_text: str, nozzle_text: str) -> Output:
    material = parse_material(material_text)
    if material is None:
        return error(f"unknown material: {material_text}")
    nozzle_c = parse_celsius(nozzle_text)
    if nozzle_c is None:
        return error(f"not a temperature: {nozzle_text}")

    verdict = nozzle_verdict(material, nozzle_c)
    low, high = material.nozzle_range()
    return Output(
        0 if verdict is Verdict.OK else 1,
        stdout=f"{verdict.value}: {material.value} prints at {low}–{high} °C\n",
    )


def log_command(path: Path) -> Output:
    try:
        log = load_log(path)
    except FileNotFoundError:
        return error(f"no such file: {path}")

    lines = [f"entries: {len(log.entries)}", f"problems: {len(log.problems)}"]
    for problem in log.problems:
        match problem.error:
            case MissingSeparator():
                reason = "missing separator"
            case BadDate():
                reason = "bad date"
            case _:
                reason = "empty text"
        lines.append(f"  line {problem.line_number}: {reason}")
    return Output(1 if log.problems else 0, stdout="".join(f"{line}\n" for line in lines))
