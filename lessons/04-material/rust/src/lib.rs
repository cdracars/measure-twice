//! Lesson 04: material.
//!
//! Rust ideas in this lesson: enums, methods on enums, exhaustive `match`,
//! `#[derive]`, and associated constants.
//!
//! `#[derive(Debug, Clone, Copy, PartialEq, Eq)]` asks the compiler to write
//! some standard behaviour for you: `Debug` lets `{:?}` print a value,
//! `Clone, Copy` let a value be copied like a number instead of moved, and
//! `PartialEq, Eq` let you compare with `==` (and `assert_eq!`).

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Material {
    Pla,
    Petg,
    Abs,
    Tpu,
}

impl Material {
    /// Every material, as a list you can loop over.
    pub const ALL: [Material; 4] = [Material::Pla, Material::Petg, Material::Abs, Material::Tpu];

    /// Density in g/cm³.
    pub fn density(self) -> f64 {
        // TODO: replace this line with your implementation.
        todo!("Material::density for {self:?}")
    }

    /// Nozzle temperature range in °C, as (min, max).
    pub fn nozzle_range(self) -> (i32, i32) {
        todo!("Material::nozzle_range for {self:?}")
    }

    pub fn needs_enclosure(self) -> bool {
        todo!("Material::needs_enclosure for {self:?}")
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    TooCold,
    Ok,
    TooHot,
}

pub fn nozzle_verdict(material: Material, nozzle_c: i32) -> Verdict {
    // TODO: write the boundary tests in tests/material.rs first, then replace this line.
    todo!("nozzle_verdict({material:?}, {nozzle_c})")
}
