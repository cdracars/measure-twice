export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;
export type Material = (typeof MATERIALS)[number];

// The result and error types. They're given: your job is to return them.

/** Either a value or an error. Check `ok` before using either. */
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

export type GramsError = "empty" | "not a number" | "negative";

export type NotEnoughFilament = { needed: number; remaining: number };

/** Grams from text like "250", "12.5 g" or " 40g ". */
export function parseGrams(text: string): Result<number, GramsError> {
  // TODO: replace this line with your implementation.
  throw new Error("TODO: implement parseGrams");
}

/** A material from text like "PLA" or " petg ". */
export function parseMaterial(text: string): Result<Material, "unknown material"> {
  // TODO: write the tests in parse.test.ts first, then replace this line.
  throw new Error("TODO: implement parseMaterial");
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
    // TODO: replace this line with your implementation.
    throw new Error("TODO: implement Spool.consume");
  }
}
