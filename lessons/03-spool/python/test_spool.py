import unittest

from spool import Spool


def full_pla_spool() -> Spool:
    return Spool("PLA", 1.75, 1.24, 1000.0)


class SpoolTest(unittest.TestCase):
    def test_a_new_spool_knows_its_material(self):
        self.assertEqual("PLA", full_pla_spool().material)

    def test_a_new_spool_knows_how_much_is_left(self):
        self.assertAlmostEqual(1000.0, full_pla_spool().grams_remaining, delta=0.01)

    def test_a_full_1_kg_pla_spool_holds_about_335_m(self):
        self.assertAlmostEqual(335_280.0, full_pla_spool().remaining_length_mm(), delta=50.0)

    def test_a_half_used_spool_holds_half_the_length(self):
        spool = Spool("PLA", 1.75, 1.24, 500.0)
        self.assertAlmostEqual(167_640.0, spool.remaining_length_mm(), delta=50.0)

    def test_a_small_job_can_print(self):
        self.assertTrue(full_pla_spool().can_print(25.0))

    def test_a_job_needing_exactly_what_is_left_can_print(self):
        self.assertTrue(full_pla_spool().can_print(1000.0))

    def test_a_job_needing_more_than_is_left_cannot_print(self):
        self.assertFalse(full_pla_spool().can_print(1000.1))

    def test_grams_remaining_is_read_only(self):
        spool = full_pla_spool()
        with self.assertRaises(AttributeError):
            spool.grams_remaining = 5000.0


class ConsumeTest(unittest.TestCase):
    """No tests yet. Write them before the code."""


if __name__ == "__main__":
    unittest.main()
