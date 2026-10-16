//! Lesson 02: nozzle temperature.
//!
//! Rust ideas in this lesson: `if`/`else if` as an expression, `match` on
//! string slices, tuples, and exhaustiveness checking.
//!
//! The return type `&'static str` means "a string literal baked into the
//! program". Lesson 07 explains the `&` and the `'static`; for now, return
//! literals like `"ok"`.

/// Whether a nozzle temperature suits a material:
/// `"too cold"`, `"ok"`, `"too hot"`, or `"unknown material"`.
pub fn nozzle_verdict(material: &str, nozzle_c: i32) -> &'static str {
    let (min, max) = match material {
        "PLA" => (190, 220),
        "PETG" => (220, 250),
        "ABS" => (230, 260),
        "TPU" => (210, 230),
        _ => return "unknown material",
    };

    if nozzle_c < min {
        "too cold"
    } else if nozzle_c > max {
        "too hot"
    } else {
        "ok"
    }
}

/// Whether a material needs an enclosed printer.
pub fn needs_enclosure(material: &str) -> bool {
    material == "ABS"
}
