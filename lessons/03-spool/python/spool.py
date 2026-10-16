import math


class Spool:
    """A reel of filament, and how much of it is left."""

    def __init__(
        self,
        material: str,
        diameter_mm: float,
        density_g_per_cm3: float,
        grams_remaining: float,
    ) -> None:
        self._material = material
        self._diameter_mm = diameter_mm
        self._density_g_per_cm3 = density_g_per_cm3
        self._grams_remaining = grams_remaining

    @property
    def material(self) -> str:
        return self._material

    @property
    def grams_remaining(self) -> float:
        return self._grams_remaining

    def remaining_length_mm(self) -> float:
        area_mm2 = math.pi * (self._diameter_mm / 2) ** 2
        grams_per_mm = area_mm2 / 1000 * self._density_g_per_cm3
        return self._grams_remaining / grams_per_mm

    def can_print(self, grams: float) -> bool:
        return grams <= self._grams_remaining

    def consume(self, grams: float) -> None:
        """Use up filament. Callers must check can_print() first."""
        self._grams_remaining -= grams
