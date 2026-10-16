/** A reel of filament, and how much of it is left. */
export class Spool {
  // TODO: declare the fields a spool needs. Make the remaining grams a
  // JavaScript private field (#gramsRemaining), so only consume() can change it.

  constructor(material: string, diameterMm: number, densityGPerCm3: number, gramsRemaining: number) {
    // TODO: replace this line with your implementation.
    throw new Error("TODO: implement the Spool constructor");
  }

  get material(): string {
    throw new Error("TODO: implement Spool.material");
  }

  get gramsRemaining(): number {
    throw new Error("TODO: implement Spool.gramsRemaining");
  }

  remainingLengthMm(): number {
    throw new Error("TODO: implement Spool.remainingLengthMm");
  }

  canPrint(grams: number): boolean {
    throw new Error("TODO: implement Spool.canPrint");
  }

  /** Use up filament. Callers must check canPrint() first. */
  consume(grams: number): void {
    // TODO: write the tests in spool.test.ts first, then replace this line.
    throw new Error("TODO: implement Spool.consume");
  }
}
