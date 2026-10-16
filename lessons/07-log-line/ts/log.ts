export type LogEntry = {
  readonly date: string;
  readonly text: string;
};

// The result and error types. They're given: your job is to return them.

export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

export type LogLineError = "missing separator" | "bad date" | "empty text";

/** A log entry from a line like "2026-10-16: replaced nozzle". */
export function parseEntry(line: string): Result<LogEntry, LogLineError> {
  // TODO: write the error tests in log.test.ts first, then replace this line.
  throw new Error("TODO: implement parseEntry");
}

/** The line for an entry: "YYYY-MM-DD: text". */
export function formatEntry(entry: LogEntry): string {
  // TODO: replace this line with your implementation.
  throw new Error("TODO: implement formatEntry");
}

/**
 * The text if it has at most maxChars characters, otherwise its first
 * maxChars characters followed by "…".
 */
export function truncate(text: string, maxChars: number): string {
  throw new Error("TODO: implement truncate");
}
