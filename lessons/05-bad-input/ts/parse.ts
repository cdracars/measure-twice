export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;
export type Material = (typeof MATERIALS)[number];

// The result and error types. They're given: your job is to return them.

/** Either a value or an error. Check `ok` before using either. */
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

export type GramsError = "empty" | "not a number" | "negative";

export type NotEnoughFilament = { needed: number; remaining: number };

/** Grams from text like "250", "12.5 g" or " 40g ". */
export function parseGrams(text: string): Result<number, GramsError> {
  const trimmed = text.trim();
  if (trimmed === "") return { ok: false, error: "empty" };

  const number = trimmed.endsWith("g") ? trimmed.slice(0, -1).trimEnd() : trimmed;
  if (!/^-?\d+(\.\d+)?$/.test(number)) return { ok: false, error: "not a number" };

  const grams = Number(number);
  if (grams < 0) return { ok: false, error: "negative" };
  return { ok: true, value: grams };
}

/** A material from text like "PLA" or " petg ". */
export function parseMaterial(text: string): Result<Material, "unknown material"> {
  const name = text.trim().toUpperCase();
  const material = MATERIALS.find((m) => m === name);
  return material === undefined ? { ok: false, error: "unknown material" } : { ok: true, value: material };
}

export class Spool {
  #gramsRemaining: number;

  constructor(gramsRemaining: number) {
    this.#gramsRemaining = gramsRemaining;
  }

  get gramsRemaining(): number {
    return this.#gramsRemaining;
  }

  /** Use up filament, or return an error and leave the spool unchanged. */
  consume(grams: number): Result<void, NotEnoughFilament> {
    if (grams > this.#gramsRemaining) {
      return { ok: false, error: { needed: grams, remaining: this.#gramsRemaining } };
    }
    this.#gramsRemaining -= grams;
    return { ok: true, value: undefined };
  }
}
