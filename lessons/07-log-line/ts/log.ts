export type LogEntry = {
  readonly date: string;
  readonly text: string;
};

// The result and error types. They're given: your job is to return them.

export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

export type LogLineError = "missing separator" | "bad date" | "empty text";

/** A log entry from a line like "2026-10-16: replaced nozzle". */
export function parseEntry(line: string): Result<LogEntry, LogLineError> {
  const colon = line.indexOf(":");
  if (colon === -1) return { ok: false, error: "missing separator" };

  const date = line.slice(0, colon).trim();
  const text = line.slice(colon + 1).trim();
  if (!isValidDate(date)) return { ok: false, error: "bad date" };
  if (text === "") return { ok: false, error: "empty text" };
  return { ok: true, value: { date, text } };
}

/** Whether a string looks like YYYY-MM-DD. Checks the shape, not the calendar. */
function isValidDate(date: string): boolean {
  const match = /^\d{4}-(\d{2})-(\d{2})$/.exec(date);
  if (match === null) return false;
  const month = Number(match[1]);
  const day = Number(match[2]);
  return month >= 1 && month <= 12 && day >= 1 && day <= 31;
}

/** The line for an entry: "YYYY-MM-DD: text". */
export function formatEntry(entry: LogEntry): string {
  return `${entry.date}: ${entry.text}`;
}

/**
 * The text if it has at most maxChars characters, otherwise its first
 * maxChars characters followed by "…".
 */
export function truncate(text: string, maxChars: number): string {
  // Spreading a string splits it into code points, so an emoji stays whole.
  const chars = [...text];
  if (chars.length <= maxChars) return text;
  return chars.slice(0, maxChars).join("") + "…";
}
