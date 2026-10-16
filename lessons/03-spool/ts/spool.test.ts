import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { Spool } from "./spool.ts";

function assertClose(expected: number, actual: number, tolerance = 0.01): void {
  assert.ok(
    Math.abs(expected - actual) <= tolerance,
    `expected ${expected} (± ${tolerance}), got ${actual}`,
  );
}

function fullPlaSpool(): Spool {
  return new Spool("PLA", 1.75, 1.24, 1000);
}

describe("Spool", () => {
  test("a new spool knows its material", () => {
    assert.equal(fullPlaSpool().material, "PLA");
  });

  test("a new spool knows how much is left", () => {
    assertClose(1000, fullPlaSpool().gramsRemaining);
  });

  test("a full 1 kg PLA spool holds about 335 m", () => {
    assertClose(335_280, fullPlaSpool().remainingLengthMm(), 50);
  });

  test("a half-used spool holds half the length", () => {
    const spool = new Spool("PLA", 1.75, 1.24, 500);
    assertClose(167_640, spool.remainingLengthMm(), 50);
  });

  test("a small job can print", () => {
    assert.equal(fullPlaSpool().canPrint(25), true);
  });

  test("a job needing exactly what is left can print", () => {
    assert.equal(fullPlaSpool().canPrint(1000), true);
  });

  test("a job needing more than is left cannot print", () => {
    assert.equal(fullPlaSpool().canPrint(1000.1), false);
  });

  test("remaining grams cannot be set from outside", () => {
    const spool = fullPlaSpool();
    // A getter with no setter: assigning throws in strict mode (all ES modules).
    assert.throws(() => {
      (spool as { gramsRemaining: number }).gramsRemaining = 5000;
    }, TypeError);
  });
});

// consume: no tests yet. Write them before the code.
describe("consume", () => {});
