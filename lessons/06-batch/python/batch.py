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
    return sum(job.grams for job in jobs)


def grams_by_material(jobs: list[Job]) -> dict[Material, float]:
    """Total grams per material, for the materials that appear."""
    totals: dict[Material, float] = {}
    for job in jobs:
        totals[job.material] = totals.get(job.material, 0.0) + job.grams
    return totals


def heaviest_job(jobs: list[Job]) -> Job | None:
    """The job with the most grams, or None if there are none. The first wins ties."""
    # max() returns the first of several equal items.
    return max(jobs, key=lambda job: job.grams, default=None)


def jobs_using(jobs: list[Job], material: Material) -> list[str]:
    """Names of the jobs using a material, in their original order."""
    return [job.name for job in jobs if job.material is material]
