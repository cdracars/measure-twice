from enum import Enum


class Material(Enum):
    PLA = "PLA"
    PETG = "PETG"
    ABS = "ABS"
    TPU = "TPU"

    def density(self) -> float:
        """Density in g/cm³."""
        match self:
            case Material.PLA:
                return 1.24
            case Material.PETG:
                return 1.27
            case Material.ABS:
                return 1.04
            case Material.TPU:
                return 1.21

    def nozzle_range(self) -> tuple[int, int]:
        """Nozzle temperature range in °C, as (min, max)."""
        match self:
            case Material.PLA:
                return (190, 220)
            case Material.PETG:
                return (220, 250)
            case Material.ABS:
                return (230, 260)
            case Material.TPU:
                return (210, 230)

    def needs_enclosure(self) -> bool:
        return self is Material.ABS


class Verdict(Enum):
    TOO_COLD = "too cold"
    OK = "ok"
    TOO_HOT = "too hot"


def nozzle_verdict(material: Material, nozzle_c: int) -> Verdict:
    low, high = material.nozzle_range()
    if nozzle_c < low:
        return Verdict.TOO_COLD
    if nozzle_c > high:
        return Verdict.TOO_HOT
    return Verdict.OK
