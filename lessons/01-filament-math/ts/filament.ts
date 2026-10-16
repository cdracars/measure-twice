/** Grams per millimetre of filament. */
function gramsPerMm(diameterMm: number, densityGPerCm3: number): number {
  const areaMm2 = Math.PI * (diameterMm / 2) ** 2;
  const cm3PerMm = areaMm2 / 1000;
  return cm3PerMm * densityGPerCm3;
}

/** Weight in grams of a length of filament. */
export function filamentGrams(lengthMm: number, diameterMm: number, densityGPerCm3: number): number {
  return lengthMm * gramsPerMm(diameterMm, densityGPerCm3);
}

/** Length in millimetres of a weight of filament. */
export function filamentLengthMm(grams: number, diameterMm: number, densityGPerCm3: number): number {
  return grams / gramsPerMm(diameterMm, densityGPerCm3);
}
