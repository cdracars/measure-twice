//! Lesson 10: test frameworks.
//!
//! Lesson 01's solution. In this lesson the code is finished; the tests move
//! from `tests/` (integration tests, which see only the public API) into this
//! file (unit tests, which can see private items too), and into the
//! documentation as doc tests.

use std::f64::consts::PI;

fn grams_per_mm(diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    let area_mm2 = PI * (diameter_mm / 2.0).powi(2);
    area_mm2 / 1000.0 * density_g_per_cm3
}

/// Weight in grams of a length of filament.
///
/// # Examples
///
/// ```
/// use lesson_10_test_frameworks::filament_grams;
///
/// // One metre of 1.75 mm PLA weighs about 3 g.
/// let grams = filament_grams(1000.0, 1.75, 1.24);
/// assert!((grams - 2.98).abs() < 0.01);
/// ```
pub fn filament_grams(length_mm: f64, diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    length_mm * grams_per_mm(diameter_mm, density_g_per_cm3)
}

/// Length in millimetres of a weight of filament.
pub fn filament_length_mm(grams: f64, diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    grams / grams_per_mm(diameter_mm, density_g_per_cm3)
}

// Unit tests: compiled only for `cargo test`, and able to see private items
// such as `grams_per_mm`.
#[cfg(test)]
mod tests {
    use super::*;

    fn assert_close(expected: f64, actual: f64, tolerance: f64) {
        assert!(
            (expected - actual).abs() <= tolerance,
            "expected {expected} (± {tolerance}), got {actual}"
        );
    }

    #[test]
    fn one_metre_of_pla_weighs_about_3_g() {
        assert_close(2.98, filament_grams(1000.0, 1.75, 1.24), 0.01);
    }

    #[test]
    fn a_metre_of_filament_weighs() {
        let cases = [
            ("1.75 mm PLA", 1.75, 1.24, 2.98),
            ("2.85 mm PLA", 2.85, 1.24, 7.91),
            ("1.75 mm PETG", 1.75, 1.27, 3.05),
        ];
        for (name, diameter_mm, density, grams) in cases {
            let actual = filament_grams(1000.0, diameter_mm, density);
            assert!(
                (actual - grams).abs() <= 0.01,
                "{name}: expected {grams}, got {actual}"
            );
        }
    }

    #[test]
    fn zero_length_weighs_nothing() {
        assert_close(0.0, filament_grams(0.0, 1.75, 1.24), 0.01);
    }

    #[test]
    fn a_1_kg_spool_of_pla_holds_about_335_m() {
        assert_close(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), 50.0);
    }

    #[test]
    fn length_and_weight_convert_back_and_forth() {
        let grams = filament_grams(4200.0, 1.75, 1.24);
        assert_close(4200.0, filament_length_mm(grams, 1.75, 1.24), 0.01);
    }

    #[test]
    fn a_millimetre_of_1_75_mm_pla_weighs_about_3_mg() {
        // grams_per_mm is private: only a unit test in this file can call it.
        assert_close(0.002_98, grams_per_mm(1.75, 1.24), 0.000_01);
    }
}
