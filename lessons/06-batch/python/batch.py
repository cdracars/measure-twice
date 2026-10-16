from dataclasses import dataclass
from enum import Enum


class Material(Enum):
    PLA = "PLA"
    PETG = "PETG"
    ABS = "ABS"
    TPU = "TPU"


@dataclass(frozen=True)
class Job:
    name: str
    material: Material
    grams: float


def total_grams(jobs: list[Job]) -> float:
    # TODO: replace this line with your implementation.
    raise NotImplementedError("TODO: implement total_grams")


def grams_by_material(jobs: list[Job]) -> dict[Material, float]:
    """Total grams per material, for the materials that appear."""
    raise NotImplementedError("TODO: implement grams_by_material")


def heaviest_job(jobs: list[Job]) -> Job | None:
    """The job with the most grams, or None if there are none. The first wins ties."""
    # TODO: write the tests in test_batch.py first, then replace this line.
    raise NotImplementedError("TODO: implement heaviest_job")


def jobs_using(jobs: list[Job], material: Material) -> list[str]:
    """Names of the jobs using a material, in their original order."""
    raise NotImplementedError("TODO: implement jobs_using")
