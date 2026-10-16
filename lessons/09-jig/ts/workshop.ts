// Finished pieces from lessons 01–08. You don't need to change this file.

import { readFileSync } from "node:fs";

export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;
export type Material = (typeof MATERIALS)[number];

export type Verdict = "too cold" | "ok" | "too hot";

const DENSITY: Record<Material, number> = { PLA: 1.24, PETG: 1.27, ABS: 1.04, TPU: 1.21 };

const NOZZLE_RANGE: Record<Material, readonly [number, number]> = {
  PLA: [190, 220],
  PETG: [220, 250],
  ABS: [230, 260],
  TPU: [210, 230],
};

export function nozzleRange(material: Material): readonly [number, number] {
  return NOZZLE_RANGE[material];
}

/** The material, or undefined if the text isn't one. Ignores case and spaces. */
export function parseMaterial(text: string): Material | undefined {
  const name = text.trim().toUpperCase();
  return MATERIALS.find((m) => m === name);
}

/** A length in mm such as "1000" or "12.5", or undefined if the text isn't one. */
export function parseLengthMm(text: string): number | undefined {
  const trimmed = text.trim();
  return /^\d+(\.\d+)?$/.test(trimmed) ? Number(trimmed) : undefined;
}

/** A whole number of °C such as "205", or undefined if the text isn't one. */
export function parseCelsius(text: string): number | undefined {
  const trimmed = text.trim();
  return /^-?\d+$/.test(trimmed) ? Number(trimmed) : undefined;
}

/** Weight in grams of a length of 1.75 mm filament. */
export function filamentGrams(lengthMm: number, material: Material): number {
  const areaMm2 = Math.PI * (1.75 / 2) ** 2;
  return ((lengthMm * areaMm2) / 1000) * DENSITY[material];
}

export function nozzleVerdict(material: Material, nozzleC: number): Verdict {
  const [min, max] = nozzleRange(material);
  if (nozzleC < min) return "too cold";
  if (nozzleC > max) return "too hot";
  return "ok";
}

// The Build Log, from lessons 07 and 08.

export type LogEntry = { readonly date: string; readonly text: string };
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export type LogLineError = "missing separator" | "bad date" | "empty text";
export type Problem = { readonly lineNumber: number; readonly error: LogLineError };
export type LoadedLog = { readonly entries: LogEntry[]; readonly problems: Problem[] };

export function parseEntry(line: string): Result<LogEntry, LogLineError> {
  const colon = line.indexOf(":");
  if (colon === -1) return { ok: false, error: "missing separator" };
  const date = line.slice(0, colon).trim();
  const text = line.slice(colon + 1).trim();
  const match = /^\d{4}-(\d{2})-(\d{2})$/.exec(date);
  const month = Number(match?.[1]);
  const day = Number(match?.[2]);
  if (match === null || month < 1 || month > 12 || day < 1 || day > 31) {
    return { ok: false, error: "bad date" };
  }
  if (text === "") return { ok: false, error: "empty text" };
  return { ok: true, value: { date, text } };
}

export function loadLog(path: string): Result<LoadedLog, "not found"> {
  let text: string;
  try {
    text = readFileSync(path, "utf8");
  } catch (error) {
    if (error instanceof Error && "code" in error && error.code === "ENOENT") {
      return { ok: false, error: "not found" };
    }
    throw error;
  }
  const entries: LogEntry[] = [];
  const problems: Problem[] = [];
  text.split("\n").forEach((line, index) => {
    const trimmed = line.trim();
    if (trimmed === "" || trimmed.startsWith("#")) return;
    const result = parseEntry(line);
    if (result.ok) entries.push(result.value);
    else problems.push({ lineNumber: index + 1, error: result.error });
  });
  return { ok: true, value: { entries, problems } };
}
