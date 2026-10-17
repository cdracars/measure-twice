import unittest

from filament import filament_grams, filament_length_mm


class FilamentMathTest(unittest.TestCase):
    def test_one_metre_of_pla_weighs_about_3_g(self):
        self.assertAlmostEqual(2.98, filament_grams(1000.0, 1.75, 1.24), delta=0.01)

    def test_zero_length_weighs_nothing(self):
        self.assertAlmostEqual(0.0, filament_grams(0.0, 1.75, 1.24), delta=0.01)

    def test_thicker_filament_is_much_heavier_per_metre(self):
        self.assertAlmostEqual(7.91, filament_grams(1000.0, 2.85, 1.24), delta=0.01)

    def test_denser_material_weighs_more(self):
        self.assertAlmostEqual(3.05, filament_grams(1000.0, 1.75, 1.27), delta=0.01)

    def test_a_1_kg_spool_holds_about_335_m(self):
        self.assertAlmostEqual(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), delta=50.0)

    def test_length_and_weight_convert_back_and_forth(self):
        grams = filament_grams(4200.0, 1.75, 1.24)
        self.assertAlmostEqual(4200.0, filament_length_mm(grams, 1.75, 1.24), delta=0.01)

    # Last step of this lesson: add one test of your own here. The guide tells you when.


if __name__ == "__main__":
    unittest.main()
