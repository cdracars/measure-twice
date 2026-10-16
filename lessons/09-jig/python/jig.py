"""The entry point: the only code that touches the real terminal. Given."""

import sys

from cli import run

if __name__ == "__main__":
    output = run(sys.argv[1:])
    sys.stdout.write(output.stdout)
    sys.stderr.write(output.stderr)
    sys.exit(output.code)
