//! Lesson 03: spool.
//!
//! Rust ideas in this lesson: structs, `impl` blocks, associated functions
//! (`new`), `&self` vs `&mut self`, `String` vs `&str`, and privacy: fields
//! are private outside this module unless marked `pub`.

/// A reel of filament, and how much of it is left.
pub struct Spool {
    // TODO: add the fields a spool needs. Leave them private (no `pub`),
    // so only this module's methods can change them. For the material,
    // store an owned `String`; turn the `&str` argument into one with
    // `.to_string()`.
}

impl Spool {
    pub fn new(
        material: &str,
        diameter_mm: f64,
        density_g_per_cm3: f64,
        grams_remaining: f64,
    ) -> Spool {
        // TODO: replace this line with your implementation.
        todo!("Spool::new({material:?}, {diameter_mm}, {density_g_per_cm3}, {grams_remaining})")
    }

    pub fn material(&self) -> &str {
        todo!("Spool::material")
    }

    pub fn grams_remaining(&self) -> f64 {
        todo!("Spool::grams_remaining")
    }

    pub fn remaining_length_mm(&self) -> f64 {
        todo!("Spool::remaining_length_mm")
    }

    pub fn can_print(&self, grams: f64) -> bool {
        todo!("Spool::can_print({grams})")
    }

    /// Use up filament. Callers must check `can_print` first.
    pub fn consume(&mut self, grams: f64) {
        // TODO: write the tests in tests/spool.rs first, then replace this line.
        todo!("Spool::consume({grams})")
    }
}
