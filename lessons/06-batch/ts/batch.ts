export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;
export type Material = (typeof MATERIALS)[number];

export type Job = {
  readonly name: string;
  readonly material: Material;
  readonly grams: number;
};

export function totalGrams(jobs: readonly Job[]): number {
  // TODO: replace this line with your implementation.
  throw new Error("TODO: implement totalGrams");
}

/** Total grams per material, for the materials that appear. */
export function gramsByMaterial(jobs: readonly Job[]): Map<Material, number> {
  throw new Error("TODO: implement gramsByMaterial");
}

/** The job with the most grams, or undefined if there are none. The first wins ties. */
export function heaviestJob(jobs: readonly Job[]): Job | undefined {
  // TODO: write the tests in batch.test.ts first, then replace this line.
  throw new Error("TODO: implement heaviestJob");
}

/** Names of the jobs using a material, in their original order. */
export function jobsUsing(jobs: readonly Job[], material: Material): string[] {
  throw new Error("TODO: implement jobsUsing");
}
