from enum import Enum


class Material(Enum):
    PLA = "PLA"
    PETG = "PETG"
    ABS = "ABS"
    TPU = "TPU"


# The errors. They're given: your job is to raise them.


class InvalidAmount(ValueError):
    """Base class for every way a weight can be invalid."""


class EmptyInput(InvalidAmount):
    pass


class NotANumber(InvalidAmount):
    pass


class NegativeAmount(InvalidAmount):
    pass


class UnknownMaterial(ValueError):
    pass


class NotEnoughFilament(Exception):
    pass


def parse_grams(text: str) -> float:
    """Grams from text like "250", "12.5 g" or " 40g ".

    Raises an InvalidAmount subclass if the text isn't a valid weight.
    """
    # TODO: replace this line with your implementation.
    raise NotImplementedError("TODO: implement parse_grams")


def parse_material(text: str) -> Material:
    """A material from text like "PLA" or " petg ".

    Raises UnknownMaterial if the text isn't a known material.
    """
    # TODO: write the tests in test_parse.py first, then replace this line.
    raise NotImplementedError("TODO: implement parse_material")


class Spool:
    def __init__(self, grams_remaining: float) -> None:
        self._grams_remaining = grams_remaining

    @property
    def grams_remaining(self) -> float:
        return self._grams_remaining

    def consume(self, grams: float) -> None:
        """Use up filament, or raise NotEnoughFilament and leave the spool unchanged."""
        # TODO: replace this line with your implementation.
        raise NotImplementedError("TODO: implement Spool.consume")
