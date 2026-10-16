/** Every material, as a list you can loop over. */
export const MATERIALS = ["PLA", "PETG", "ABS", "TPU"] as const;

/** One of the values in MATERIALS: "PLA" | "PETG" | "ABS" | "TPU". */
export type Material = (typeof MATERIALS)[number];

export type Verdict = "too cold" | "ok" | "too hot";

/**
 * Fails to type-check if a switch forgot a case: only `never` is assignable
 * to `never`, and `material` is only `never` once every case is handled.
 */
function unreachable(value: never): never {
  throw new Error(`unhandled case: ${String(value)}`);
}

/** Density in g/cm³. */
export function density(material: Material): number {
  switch (material) {
    case "PLA":
      return 1.24;
    case "PETG":
      return 1.27;
    case "ABS":
      return 1.04;
    case "TPU":
      return 1.21;
    default:
      return unreachable(material);
  }
}

/** Nozzle temperature range in °C, as [min, max]. */
export function nozzleRange(material: Material): readonly [number, number] {
  switch (material) {
    case "PLA":
      return [190, 220];
    case "PETG":
      return [220, 250];
    case "ABS":
      return [230, 260];
    case "TPU":
      return [210, 230];
    default:
      return unreachable(material);
  }
}

export function needsEnclosure(material: Material): boolean {
  return material === "ABS";
}

export function nozzleVerdict(material: Material, nozzleC: number): Verdict {
  const [min, max] = nozzleRange(material);
  if (nozzleC < min) return "too cold";
  if (nozzleC > max) return "too hot";
  return "ok";
}
