/** A reel of filament, and how much of it is left. */
export class Spool {
  readonly #material: string;
  readonly #diameterMm: number;
  readonly #densityGPerCm3: number;
  #gramsRemaining: number;

  constructor(material: string, diameterMm: number, densityGPerCm3: number, gramsRemaining: number) {
    this.#material = material;
    this.#diameterMm = diameterMm;
    this.#densityGPerCm3 = densityGPerCm3;
    this.#gramsRemaining = gramsRemaining;
  }

  get material(): string {
    return this.#material;
  }

  get gramsRemaining(): number {
    return this.#gramsRemaining;
  }

  remainingLengthMm(): number {
    const areaMm2 = Math.PI * (this.#diameterMm / 2) ** 2;
    const gramsPerMm = (areaMm2 / 1000) * this.#densityGPerCm3;
    return this.#gramsRemaining / gramsPerMm;
  }

  canPrint(grams: number): boolean {
    return grams <= this.#gramsRemaining;
  }

  /** Use up filament. Callers must check canPrint() first. */
  consume(grams: number): void {
    this.#gramsRemaining -= grams;
  }
}
