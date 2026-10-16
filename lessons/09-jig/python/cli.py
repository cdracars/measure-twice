from dataclasses import dataclass

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
    # TODO: replace this line with your implementation. The pieces you need
    # are in workshop.py.
    raise NotImplementedError("TODO: implement run")
