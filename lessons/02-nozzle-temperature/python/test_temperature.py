import unittest

from temperature import needs_enclosure, nozzle_verdict


class NozzleVerdictTest(unittest.TestCase):
    def test_pla_in_the_middle_of_its_range_is_ok(self):
        self.assertEqual("ok", nozzle_verdict("PLA", 205))

    def test_pla_at_its_minimum_is_ok(self):
        self.assertEqual("ok", nozzle_verdict("PLA", 190))

    def test_pla_one_degree_below_its_minimum_is_too_cold(self):
        self.assertEqual("too cold", nozzle_verdict("PLA", 189))

    def test_pla_at_its_maximum_is_ok(self):
        self.assertEqual("ok", nozzle_verdict("PLA", 220))

    def test_pla_one_degree_above_its_maximum_is_too_hot(self):
        self.assertEqual("too hot", nozzle_verdict("PLA", 221))

    def test_petg_at_a_pla_temperature_is_too_cold(self):
        self.assertEqual("too cold", nozzle_verdict("PETG", 200))

    def test_abs_at_its_maximum_is_ok(self):
        self.assertEqual("ok", nozzle_verdict("ABS", 260))

    def test_tpu_above_its_maximum_is_too_hot(self):
        self.assertEqual("too hot", nozzle_verdict("TPU", 231))

    def test_an_unknown_material_is_reported(self):
        self.assertEqual("unknown material", nozzle_verdict("Nylon", 250))

    def test_material_names_are_exact(self):
        self.assertEqual("unknown material", nozzle_verdict("pla", 205))


class NeedsEnclosureTest(unittest.TestCase):
    """One example. Write the rest before the code."""

    def test_abs_needs_an_enclosure(self):
        self.assertTrue(needs_enclosure("ABS"))


if __name__ == "__main__":
    unittest.main()
