//! Lesson 01: filament math.
//!
//! Rust ideas in this lesson: functions, `f64`, constants from `std`, and
//! `todo!()`, a macro that compiles but panics when it runs.

use std::f64::consts::PI;

/// Grams per millimetre of filament.
fn grams_per_mm(diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    let area_mm2 = PI * (diameter_mm / 2.0).powi(2);
    let cm3_per_mm = area_mm2 / 1000.0;
    cm3_per_mm * density_g_per_cm3
}

/// Weight in grams of a length of filament.
pub fn filament_grams(length_mm: f64, diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    length_mm * grams_per_mm(diameter_mm, density_g_per_cm3)
}

/// Length in millimetres of a weight of filament.
pub fn filament_length_mm(grams: f64, diameter_mm: f64, density_g_per_cm3: f64) -> f64 {
    grams / grams_per_mm(diameter_mm, density_g_per_cm3)
}
