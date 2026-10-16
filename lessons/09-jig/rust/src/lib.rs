//! Lesson 09: jig.
//!
//! Rust ideas in this lesson: modules (`mod`, `use`), slice patterns in
//! `match` (`["grams", length, material]`), building strings with `format!`
//! and `push_str`, and a library crate with a binary next to it.

pub mod workshop;

pub const USAGE: &str = "\
usage: jig <command> [arguments]

commands:
  grams <length-mm> <material>   weight of 1.75 mm filament
  check <material> <nozzle-c>    is this nozzle temperature right?
  log <file>                     summarize a Build Log
  help                           show this message
";

/// What running jig produced: an exit code and the text for each stream.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Output {
    pub code: i32,
    pub stdout: String,
    pub stderr: String,
}

/// Run jig with the given arguments (not including the program name).
/// Never prints and never exits: it returns what should happen.
///
/// Tip: a `match` on `args` can use slice patterns:
/// `match args { ["help"] => ..., ["grams", length, material] => ..., _ => ... }`.
pub fn run(args: &[&str]) -> Output {
    // TODO: replace this line with your implementation. The pieces you need
    // are in workshop.rs, as `workshop::parse_material` and so on.
    todo!("run({args:?})")
}
