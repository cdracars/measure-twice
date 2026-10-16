import pytest
from filament import filament_grams, filament_length_mm


def test_one_metre_of_pla_weighs_about_3_g():
    assert filament_grams(1000.0, 1.75, 1.24) == pytest.approx(2.98, abs=0.01)


@pytest.mark.parametrize(
    ("diameter_mm", "density", "grams"),
    [
        pytest.param(1.75, 1.24, 2.98, id="1.75 mm PLA"),
        pytest.param(2.85, 1.24, 7.91, id="2.85 mm PLA"),
        pytest.param(1.75, 1.27, 3.05, id="1.75 mm PETG"),
    ],
)
def test_a_metre_of_filament_weighs(diameter_mm, density, grams):
    assert filament_grams(1000.0, diameter_mm, density) == pytest.approx(grams, abs=0.01)


def test_zero_length_weighs_nothing():
    assert filament_grams(0.0, 1.75, 1.24) == pytest.approx(0.0)


def test_a_1_kg_spool_of_pla_holds_about_335_m():
    assert filament_length_mm(1000.0, 1.75, 1.24) == pytest.approx(335_280.0, abs=50.0)


def test_length_and_weight_convert_back_and_forth():
    grams = filament_grams(4200.0, 1.75, 1.24)
    assert filament_length_mm(grams, 1.75, 1.24) == pytest.approx(4200.0)
