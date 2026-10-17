import assert from "node:assert/strict";
import { test } from "node:test";

import { filamentGrams, filamentLengthMm } from "./filament.ts";

function assertClose(expected: number, actual: number, tolerance = 0.01): void {
  assert.ok(
    Math.abs(expected - actual) <= tolerance,
    `expected ${expected} (± ${tolerance}), got ${actual}`,
  );
}

test("one metre of 1.75 mm PLA weighs about 3 g", () => {
  assertClose(2.98, filamentGrams(1000, 1.75, 1.24));
});

test("zero length weighs nothing", () => {
  assertClose(0, filamentGrams(0, 1.75, 1.24));
});

test("2.85 mm filament is much heavier per metre", () => {
  assertClose(7.91, filamentGrams(1000, 2.85, 1.24));
});

test("denser material weighs more (PETG)", () => {
  assertClose(3.05, filamentGrams(1000, 1.75, 1.27));
});

test("a 1 kg spool of 1.75 mm PLA holds about 335 m", () => {
  assertClose(335_280, filamentLengthMm(1000, 1.75, 1.24), 50);
});

test("length and weight convert back and forth", () => {
  const grams = filamentGrams(4200, 1.75, 1.24);
  assertClose(4200, filamentLengthMm(grams, 1.75, 1.24));
});

// Last step of this lesson: add one test of your own here. The guide tells you when.

test("one metre of 1.75 mm TPU weighs about 2.91 g", () => {
  assertClose(2.91, filamentGrams(1000, 1.75, 1.21));
});
