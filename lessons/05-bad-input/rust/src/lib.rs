//! Lesson 05: bad input.
//!
//! Rust ideas in this lesson: `Result<T, E>`, error enums, `?`, `str` methods
//! (`trim`, `strip_suffix`, `eq_ignore_ascii_case`), and `f64::is_finite`.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Material {
    Pla,
    Petg,
    Abs,
    Tpu,
}

// The errors. They're given: your job is to return them.

/// Every way a weight can be invalid.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GramsError {
    Empty,
    NotANumber,
    Negative,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnknownMaterial(pub String);

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct NotEnoughFilament {
    pub needed: f64,
    pub remaining: f64,
}

/// Grams from text like `"250"`, `"12.5 g"` or `" 40g "`.
pub fn parse_grams(text: &str) -> Result<f64, GramsError> {
    // TODO: replace this line with your implementation.
    todo!("parse_grams({text:?})")
}

/// A material from text like `"PLA"` or `" petg "`.
pub fn parse_material(text: &str) -> Result<Material, UnknownMaterial> {
    // TODO: write the tests in tests/parse.rs first, then replace this line.
    todo!("parse_material({text:?})")
}

pub struct Spool {
    grams_remaining: f64,
}

impl Spool {
    pub fn new(grams_remaining: f64) -> Spool {
        Spool { grams_remaining }
    }

    pub fn grams_remaining(&self) -> f64 {
        self.grams_remaining
    }

    /// Use up filament, or return an error and leave the spool unchanged.
    pub fn consume(&mut self, grams: f64) -> Result<(), NotEnoughFilament> {
        // TODO: replace this line with your implementation.
        todo!("Spool::consume({grams})")
    }
}
