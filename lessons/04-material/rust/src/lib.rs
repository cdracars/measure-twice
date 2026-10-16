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
        match self {
            Material::Pla => 1.24,
            Material::Petg => 1.27,
            Material::Abs => 1.04,
            Material::Tpu => 1.21,
        }
    }

    /// Nozzle temperature range in °C, as (min, max).
    pub fn nozzle_range(self) -> (i32, i32) {
        match self {
            Material::Pla => (190, 220),
            Material::Petg => (220, 250),
            Material::Abs => (230, 260),
            Material::Tpu => (210, 230),
        }
    }

    pub fn needs_enclosure(self) -> bool {
        self == Material::Abs
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    TooCold,
    Ok,
    TooHot,
}

pub fn nozzle_verdict(material: Material, nozzle_c: i32) -> Verdict {
    let (min, max) = material.nozzle_range();
    if nozzle_c < min {
        Verdict::TooCold
    } else if nozzle_c > max {
        Verdict::TooHot
    } else {
        Verdict::Ok
    }
}
