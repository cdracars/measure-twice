export const USAGE = `usage: jig <command> [arguments]

commands:
  grams <length-mm> <material>   weight of 1.75 mm filament
  check <material> <nozzle-c>    is this nozzle temperature right?
  log <file>                     summarize a Build Log
  help                           show this message
`;

/** What running jig produced: an exit code and the text for each stream. */
export type Output = { code: number; stdout: string; stderr: string };

/**
 * Run jig with the given arguments (not including the program name).
 * Never prints and never exits: it returns what should happen.
 */
export function run(args: readonly string[]): Output {
  // TODO: replace this line with your implementation. The pieces you need
  // are in workshop.ts.
  throw new Error("TODO: implement run");
}
