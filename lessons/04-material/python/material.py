from enum import Enum


class Material(Enum):
    PLA = "PLA"
    PETG = "PETG"
    ABS = "ABS"
    TPU = "TPU"

    def density(self) -> float:
        """Density in g/cm³."""
        # TODO: replace this line with your implementation.
        raise NotImplementedError("TODO: implement Material.density")

    def nozzle_range(self) -> tuple[int, int]:
        """Nozzle temperature range in °C, as (min, max)."""
        raise NotImplementedError("TODO: implement Material.nozzle_range")

    def needs_enclosure(self) -> bool:
        raise NotImplementedError("TODO: implement Material.needs_enclosure")


class Verdict(Enum):
    TOO_COLD = "too cold"
    OK = "ok"
    TOO_HOT = "too hot"


def nozzle_verdict(material: Material, nozzle_c: int) -> Verdict:
    # TODO: write the boundary tests in test_material.py first, then replace this line.
    raise NotImplementedError("TODO: implement nozzle_verdict")
