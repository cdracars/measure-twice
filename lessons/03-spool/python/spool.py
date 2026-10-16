class Spool:
    """A reel of filament, and how much of it is left."""

    def __init__(
        self,
        material: str,
        diameter_mm: float,
        density_g_per_cm3: float,
        grams_remaining: float,
    ) -> None:
        # TODO: store the values. Name the remaining grams _grams_remaining,
        # so the convention says "don't touch this from outside".
        raise NotImplementedError("TODO: implement Spool.__init__")

    @property
    def material(self) -> str:
        raise NotImplementedError("TODO: implement Spool.material")

    @property
    def grams_remaining(self) -> float:
        raise NotImplementedError("TODO: implement Spool.grams_remaining")

    def remaining_length_mm(self) -> float:
        raise NotImplementedError("TODO: implement Spool.remaining_length_mm")

    def can_print(self, grams: float) -> bool:
        raise NotImplementedError("TODO: implement Spool.can_print")

    def consume(self, grams: float) -> None:
        """Use up filament. Callers must check can_print() first."""
        # TODO: write the tests in test_spool.py first, then replace this line.
        raise NotImplementedError("TODO: implement Spool.consume")
