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
    // TODO: replace this line with your implementation.
    todo!("implement nozzle_verdict({material:?}, {nozzle_c})")
}

/// Whether a material needs an enclosed printer.
pub fn needs_enclosure(material: &str) -> bool {
    // TODO: write the tests in tests/temperature.rs first, then replace this line.
    todo!("implement needs_enclosure({material:?})")
}
