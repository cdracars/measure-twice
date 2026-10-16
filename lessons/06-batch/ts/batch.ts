export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;
export type Material = (typeof MATERIALS)[number];

export type Job = {
  readonly name: string;
  readonly material: Material;
  readonly grams: number;
};

export function totalGrams(jobs: readonly Job[]): number {
  return jobs.reduce((total, job) => total + job.grams, 0);
}

/** Total grams per material, for the materials that appear. */
export function gramsByMaterial(jobs: readonly Job[]): Map<Material, number> {
  const totals = new Map<Material, number>();
  for (const job of jobs) {
    totals.set(job.material, (totals.get(job.material) ?? 0) + job.grams);
  }
  return totals;
}

/** The job with the most grams, or undefined if there are none. The first wins ties. */
export function heaviestJob(jobs: readonly Job[]): Job | undefined {
  let heaviest: Job | undefined;
  for (const job of jobs) {
    // Strictly greater, so the first of several equal jobs stays.
    if (heaviest === undefined || job.grams > heaviest.grams) heaviest = job;
  }
  return heaviest;
}

/** Names of the jobs using a material, in their original order. */
export function jobsUsing(jobs: readonly Job[], material: Material): string[] {
  return jobs.filter((job) => job.material === material).map((job) => job.name);
}
