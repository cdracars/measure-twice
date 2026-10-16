import { appendFileSync, readFileSync } from "node:fs";

// From lesson 07, finished.

export type LogEntry = { readonly date: string; readonly text: string };

export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

export type LogLineError = "missing separator" | "bad date" | "empty text";

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

export function formatEntry(entry: LogEntry): string {
  return `${entry.date}: ${entry.text}`;
}

// New in this lesson.

/** One bad line in a log file. */
export type Problem = { readonly lineNumber: number; readonly error: LogLineError };

/** Everything read from a log file: the good entries and the bad lines. */
export type LoadedLog = { readonly entries: LogEntry[]; readonly problems: Problem[] };

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

export function appendEntry(path: string, entry: LogEntry): void {
  appendFileSync(path, `${formatEntry(entry)}\n`, "utf8");
}
