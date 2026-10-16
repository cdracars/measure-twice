/**
 * Whether a nozzle temperature suits a material:
 * "too cold", "ok", "too hot", or "unknown material".
 */
export function nozzleVerdict(material: string, nozzleC: number): string {
  let min: number;
  let max: number;
  switch (material) {
    case "PLA":
      [min, max] = [190, 220];
      break;
    case "PETG":
      [min, max] = [220, 250];
      break;
    case "ABS":
      [min, max] = [230, 260];
      break;
    case "TPU":
      [min, max] = [210, 230];
      break;
    default:
      return "unknown material";
  }

  if (nozzleC < min) return "too cold";
  if (nozzleC > max) return "too hot";
  return "ok";
}

/** Whether a material needs an enclosed printer. */
export function needsEnclosure(material: string): boolean {
  return material === "ABS";
}
