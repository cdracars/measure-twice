import { describe, expect, it } from "vitest";

import { filamentGrams, filamentLengthMm } from "./filament.ts";

describe("filament math", () => {
  it("one metre of 1.75 mm PLA weighs about 3 g", () => {
    // toBeCloseTo(value, digits = 2) passes when the difference is below
    // 10^-digits / 2: here, 0.005.
    expect(filamentGrams(1000, 1.75, 1.24)).toBeCloseTo(2.98);
  });

  it.each([
    { name: "1.75 mm PLA", diameterMm: 1.75, density: 1.24, grams: 2.98 },
    { name: "2.85 mm PLA", diameterMm: 2.85, density: 1.24, grams: 7.91 },
    { name: "1.75 mm PETG", diameterMm: 1.75, density: 1.27, grams: 3.05 },
  ])("a metre of $name weighs $grams g", ({ diameterMm, density, grams }) => {
    expect(filamentGrams(1000, diameterMm, density)).toBeCloseTo(grams, 1);
  });

  it("zero length weighs nothing", () => {
    expect(filamentGrams(0, 1.75, 1.24)).toBe(0);
  });

  it("a 1 kg spool of 1.75 mm PLA holds about 335 m", () => {
    // toBeCloseTo counts decimal places, so a ± 50 tolerance is written out.
    expect(Math.abs(filamentLengthMm(1000, 1.75, 1.24) - 335_280)).toBeLessThanOrEqual(50);
  });

  it("length and weight convert back and forth", () => {
    const grams = filamentGrams(4200, 1.75, 1.24);
    expect(filamentLengthMm(grams, 1.75, 1.24)).toBeCloseTo(4200);
  });
});
