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
/// TODO: add an `# Examples` section here with a doc test. `cargo test` runs
/// the code in it, so the example in the documentation can never go stale.
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

    // TODO: port the rest of lesson 01's tests (lessons/01-filament-math/rust/tests/filament.rs).
    // Add one test that checks the private grams_per_mm directly.
}
