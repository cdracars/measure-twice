// Lesson 01's solution. In this lesson the code is finished; the tests move.

function gramsPerMm(diameterMm: number, densityGPerCm3: number): number {
  const areaMm2 = Math.PI * (diameterMm / 2) ** 2;
  return (areaMm2 / 1000) * densityGPerCm3;
}

/** Weight in grams of a length of filament. */
export function filamentGrams(lengthMm: number, diameterMm: number, densityGPerCm3: number): number {
  return lengthMm * gramsPerMm(diameterMm, densityGPerCm3);
}

/** Length in millimetres of a weight of filament. */
export function filamentLengthMm(grams: number, diameterMm: number, densityGPerCm3: number): number {
  return grams / gramsPerMm(diameterMm, densityGPerCm3);
}
