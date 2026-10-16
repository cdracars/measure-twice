//! Lesson 03: spool.
//!
//! Rust ideas in this lesson: structs, `impl` blocks, associated functions
//! (`new`), `&self` vs `&mut self`, `String` vs `&str`, and privacy: fields
//! are private outside this module unless marked `pub`.

use std::f64::consts::PI;

/// A reel of filament, and how much of it is left.
pub struct Spool {
    material: String,
    diameter_mm: f64,
    density_g_per_cm3: f64,
    grams_remaining: f64,
}

impl Spool {
    pub fn new(
        material: &str,
        diameter_mm: f64,
        density_g_per_cm3: f64,
        grams_remaining: f64,
    ) -> Spool {
        Spool {
            material: material.to_string(),
            diameter_mm,
            density_g_per_cm3,
            grams_remaining,
        }
    }

    pub fn material(&self) -> &str {
        &self.material
    }

    pub fn grams_remaining(&self) -> f64 {
        self.grams_remaining
    }

    pub fn remaining_length_mm(&self) -> f64 {
        let area_mm2 = PI * (self.diameter_mm / 2.0).powi(2);
        let grams_per_mm = area_mm2 / 1000.0 * self.density_g_per_cm3;
        self.grams_remaining / grams_per_mm
    }

    pub fn can_print(&self, grams: f64) -> bool {
        grams <= self.grams_remaining
    }

    /// Use up filament. Callers must check `can_print` first.
    pub fn consume(&mut self, grams: f64) {
        self.grams_remaining -= grams;
    }
}
