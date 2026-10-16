/** Every material, as a list you can loop over. */
export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;

/** One of the values in MATERIALS: "PLA" | "PETG" | "ABS" | "TPU". */
export type Material = (typeof MATERIALS)[number];

export type Verdict = "too cold" | "ok" | "too hot";

/** Density in g/cm³. */
export function density(material: Material): number {
  // TODO: replace this line with your implementation.
  throw new Error("TODO: implement density");
}

/** Nozzle temperature range in °C, as [min, max]. */
export function nozzleRange(material: Material): readonly [number, number] {
  throw new Error("TODO: implement nozzleRange");
}

export function needsEnclosure(material: Material): boolean {
  throw new Error("TODO: implement needsEnclosure");
}

export function nozzleVerdict(material: Material, nozzleC: number): Verdict {
  // TODO: write the boundary tests in material.test.ts first, then replace this line.
  throw new Error("TODO: implement nozzleVerdict");
}
