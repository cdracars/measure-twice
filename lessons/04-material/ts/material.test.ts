import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { MATERIALS, type Material, density, needsEnclosure, nozzleRange, nozzleVerdict } from "./material.ts";

function assertClose(expected: number, actual: number, tolerance = 0.001): void {
  assert.ok(
    Math.abs(expected - actual) <= tolerance,
    `expected ${expected} (± ${tolerance}), got ${actual}`,
  );
}

describe("Material", () => {
  const densities: Record<Material, number> = { PLA: 1.24, PETG: 1.27, ABS: 1.04, TPU: 1.21 };
  for (const material of MATERIALS) {
    test(`${material} density`, () => {
      assertClose(densities[material], density(material));
    });
  }

  test("PLA nozzle range", () => {
    assert.deepEqual(nozzleRange("PLA"), [190, 220]);
  });

  test("every nozzle range runs from low to high", () => {
    for (const material of MATERIALS) {
      const [min, max] = nozzleRange(material);
      assert.ok(min < max, `${material}: ${min} is not below ${max}`);
    }
  });

  test("ABS needs an enclosure", () => {
    assert.equal(needsEnclosure("ABS"), true);
  });

  test("no other material needs an enclosure", () => {
    for (const material of MATERIALS.filter((m) => m !== "ABS")) {
      assert.equal(needsEnclosure(material), false, material);
    }
  });
});

// One example. Write the boundary tests before the code.
describe("nozzleVerdict", () => {
  test("PLA in the middle of its range is OK", () => {
    assert.equal(nozzleVerdict("PLA", 205), "ok");
  });
});
