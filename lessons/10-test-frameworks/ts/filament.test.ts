import { describe, expect, it } from "vitest";

import { filamentGrams } from "./filament.ts";

describe("filament math", () => {
  it("one metre of 1.75 mm PLA weighs about 3 g", () => {
    // toBeCloseTo(value, digits = 2) passes when the difference is below
    // 10^-digits / 2: here, 0.005.
    expect(filamentGrams(1000, 1.75, 1.24)).toBeCloseTo(2.98);
  });

  // TODO: port the rest of lesson 01's tests (lessons/01-filament-math/ts/filament.test.ts).
  // Use it.each for the "grams of a metre" cases.
});
