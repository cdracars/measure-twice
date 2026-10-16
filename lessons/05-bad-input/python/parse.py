import re
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
    text = text.strip()
    if not text:
        raise EmptyInput("no weight given")

    number = text.removesuffix("g").rstrip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", number):
        raise NotANumber(f"not a weight: {text!r}")

    grams = float(number)
    if grams < 0:
        raise NegativeAmount(f"weight can't be negative: {text!r}")
    return grams


def parse_material(text: str) -> Material:
    """A material from text like "PLA" or " petg ".

    Raises UnknownMaterial if the text isn't a known material.
    """
    try:
        return Material(text.strip().upper())
    except ValueError:
        raise UnknownMaterial(f"unknown material: {text!r}") from None


class Spool:
    def __init__(self, grams_remaining: float) -> None:
        self._grams_remaining = grams_remaining

    @property
    def grams_remaining(self) -> float:
        return self._grams_remaining

    def consume(self, grams: float) -> None:
        """Use up filament, or raise NotEnoughFilament and leave the spool unchanged."""
        if grams > self._grams_remaining:
            raise NotEnoughFilament(f"need {grams} g, only {self._grams_remaining} g left")
        self._grams_remaining -= grams
