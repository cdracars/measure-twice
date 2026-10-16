"""Lesson 01's solution. In this lesson the code is finished; the tests move."""

import math


def grams_per_mm(diameter_mm: float, density_g_per_cm3: float) -> float:
    area_mm2 = math.pi * (diameter_mm / 2) ** 2
    return area_mm2 / 1000 * density_g_per_cm3


def filament_grams(length_mm: float, diameter_mm: float, density_g_per_cm3: float) -> float:
    """Weight in grams of a length of filament."""
    return length_mm * grams_per_mm(diameter_mm, density_g_per_cm3)


def filament_length_mm(grams: float, diameter_mm: float, density_g_per_cm3: float) -> float:
    """Length in millimetres of a weight of filament."""
    return grams / grams_per_mm(diameter_mm, density_g_per_cm3)
