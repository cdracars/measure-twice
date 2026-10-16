import unittest

from material import Material, Verdict, nozzle_verdict


class MaterialTest(unittest.TestCase):
    def test_densities(self):
        expected = {
            Material.PLA: 1.24,
            Material.PETG: 1.27,
            Material.ABS: 1.04,
            Material.TPU: 1.21,
        }
        for material, density in expected.items():
            with self.subTest(material=material):
                self.assertAlmostEqual(density, material.density(), delta=0.001)

    def test_pla_nozzle_range(self):
        self.assertEqual((190, 220), Material.PLA.nozzle_range())

    def test_every_nozzle_range_runs_from_low_to_high(self):
        for material in Material:
            with self.subTest(material=material):
                low, high = material.nozzle_range()
                self.assertLess(low, high)

    def test_abs_needs_an_enclosure(self):
        self.assertTrue(Material.ABS.needs_enclosure())

    def test_no_other_material_needs_an_enclosure(self):
        for material in Material:
            if material is not Material.ABS:
                with self.subTest(material=material):
                    self.assertFalse(material.needs_enclosure())


class NozzleVerdictTest(unittest.TestCase):
    """One example. Write the boundary tests before the code."""

    def test_pla_in_the_middle_of_its_range_is_ok(self):
        self.assertIs(Verdict.OK, nozzle_verdict(Material.PLA, 205))


if __name__ == "__main__":
    unittest.main()
