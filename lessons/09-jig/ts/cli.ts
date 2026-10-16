import {
  filamentGrams,
  loadLog,
  nozzleRange,
  nozzleVerdict,
  parseCelsius,
  parseLengthMm,
  parseMaterial,
} from "./workshop.ts";

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
  const [command, ...rest] = args;
  switch (command) {
    case undefined:
      return { code: 2, stdout: "", stderr: USAGE };
    case "help":
      return { code: 0, stdout: USAGE, stderr: "" };
    case "grams":
      return gramsCommand(rest);
    case "check":
      return checkCommand(rest);
    case "log":
      return logCommand(rest);
    default:
      return error(`unknown command: ${command}\nrun 'jig help' to see the commands`);
  }
}

function error(message: string): Output {
  return { code: 2, stdout: "", stderr: `jig: ${message}\n` };
}

function gramsCommand(args: readonly string[]): Output {
  const [lengthText, materialText] = args;
  if (args.length !== 2 || lengthText === undefined || materialText === undefined) {
    return error("usage: jig grams <length-mm> <material>");
  }
  const length = parseLengthMm(lengthText);
  if (length === undefined) return error(`not a length: ${lengthText}`);
  const material = parseMaterial(materialText);
  if (material === undefined) return error(`unknown material: ${materialText}`);
  return { code: 0, stdout: `${filamentGrams(length, material).toFixed(2)} g\n`, stderr: "" };
}

function checkCommand(args: readonly string[]): Output {
  const [materialText, nozzleText] = args;
  if (args.length !== 2 || materialText === undefined || nozzleText === undefined) {
    return error("usage: jig check <material> <nozzle-c>");
  }
  const material = parseMaterial(materialText);
  if (material === undefined) return error(`unknown material: ${materialText}`);
  const nozzleC = parseCelsius(nozzleText);
  if (nozzleC === undefined) return error(`not a temperature: ${nozzleText}`);

  const verdict = nozzleVerdict(material, nozzleC);
  const [min, max] = nozzleRange(material);
  return {
    code: verdict === "ok" ? 0 : 1,
    stdout: `${verdict}: ${material} prints at ${min}–${max} °C\n`,
    stderr: "",
  };
}

function logCommand(args: readonly string[]): Output {
  const [path] = args;
  if (args.length !== 1 || path === undefined) return error("usage: jig log <file>");

  const result = loadLog(path);
  if (!result.ok) return error(`no such file: ${path}`);

  const { entries, problems } = result.value;
  const lines = [
    `entries: ${entries.length}`,
    `problems: ${problems.length}`,
    ...problems.map((p) => `  line ${p.lineNumber}: ${p.error}`),
  ];
  return { code: problems.length === 0 ? 0 : 1, stdout: lines.map((line) => `${line}\n`).join(""), stderr: "" };
}
