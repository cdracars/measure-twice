import pytest
from filament import filament_grams


def test_one_metre_of_pla_weighs_about_3_g():
    assert filament_grams(1000.0, 1.75, 1.24) == pytest.approx(2.98, abs=0.01)


# TODO: port the rest of lesson 01's tests (lessons/01-filament-math/python/test_filament.py).
# Use @pytest.mark.parametrize for the "grams of a metre" cases.
