import unittest

from parse import (
    EmptyInput,
    InvalidAmount,
    Material,
    NegativeAmount,
    NotANumber,
    NotEnoughFilament,
    Spool,
    UnknownMaterial,
    parse_grams,
    parse_material,
)


class ParseGramsTest(unittest.TestCase):
    def test_accepted(self):
        cases = {
            "250": 250.0,
            "12.5": 12.5,
            "12.5 g": 12.5,
            "40g": 40.0,
            " 40g ": 40.0,
            "0": 0.0,
        }
        for text, grams in cases.items():
            with self.subTest(text=text):
                self.assertEqual(grams, parse_grams(text))

    def test_rejected(self):
        cases = {
            "": EmptyInput,
            "   ": EmptyInput,
            "abc": NotANumber,
            "12.5 kg": NotANumber,
            "nan": NotANumber,
            "inf": NotANumber,
            "0x10": NotANumber,
            "1_000": NotANumber,
            "-5": NegativeAmount,
            "-5 g": NegativeAmount,
        }
        for text, error in cases.items():
            with self.subTest(text=text), self.assertRaises(error):
                parse_grams(text)

    def test_every_grams_error_can_be_caught_as_invalid_amount(self):
        with self.assertRaises(InvalidAmount):
            parse_grams("abc")


class ConsumeTest(unittest.TestCase):
    def test_consuming_what_is_available_works(self):
        spool = Spool(100.0)
        spool.consume(40.0)
        self.assertEqual(60.0, spool.grams_remaining)

    def test_consuming_exactly_what_is_left_works(self):
        spool = Spool(100.0)
        spool.consume(100.0)
        self.assertEqual(0.0, spool.grams_remaining)

    def test_consuming_more_than_is_left_is_refused(self):
        spool = Spool(100.0)
        with self.assertRaises(NotEnoughFilament):
            spool.consume(100.5)

    def test_a_refused_consume_leaves_the_spool_unchanged(self):
        spool = Spool(100.0)
        with self.assertRaises(NotEnoughFilament):
            spool.consume(150.0)
        self.assertEqual(100.0, spool.grams_remaining)


class ParseMaterialTest(unittest.TestCase):
    """One example. Write the rest before the code."""

    def test_accepts_pla(self):
        self.assertIs(Material.PLA, parse_material("PLA"))

    def test_ignores_case(self):
        self.assertIs(Material.PETG, parse_material("petg"))
        self.assertIs(Material.TPU, parse_material("Tpu"))

    def test_ignores_surrounding_spaces(self):
        self.assertIs(Material.ABS, parse_material("  ABS "))

    def test_rejects_an_unknown_material(self):
        with self.assertRaises(UnknownMaterial):
            parse_material("Nylon")

    def test_rejects_empty_input(self):
        with self.assertRaises(UnknownMaterial):
            parse_material("")


if __name__ == "__main__":
    unittest.main()
