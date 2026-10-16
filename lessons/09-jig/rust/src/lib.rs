//! Lesson 09: jig.
//!
//! Rust ideas in this lesson: modules (`mod`, `use`), slice patterns in
//! `match` (`["grams", length, material]`), building strings with `format!`
//! and `push_str`, and a library crate with a binary next to it.

pub mod workshop;

use std::path::Path;

use workshop::{LogLineError, Verdict};

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
    match args {
        [] => Output {
            code: 2,
            stderr: USAGE.to_string(),
            ..Output::default()
        },
        ["help", ..] => Output {
            code: 0,
            stdout: USAGE.to_string(),
            ..Output::default()
        },
        ["grams", length, material] => grams_command(length, material),
        ["grams", ..] => error("usage: jig grams <length-mm> <material>"),
        ["check", material, nozzle] => check_command(material, nozzle),
        ["check", ..] => error("usage: jig check <material> <nozzle-c>"),
        ["log", path] => log_command(Path::new(path)),
        ["log", ..] => error("usage: jig log <file>"),
        [command, ..] => error(&format!(
            "unknown command: {command}\nrun 'jig help' to see the commands"
        )),
    }
}

fn error(message: &str) -> Output {
    Output {
        code: 2,
        stderr: format!("jig: {message}\n"),
        ..Output::default()
    }
}

fn grams_command(length_text: &str, material_text: &str) -> Output {
    let Some(length) = workshop::parse_length_mm(length_text) else {
        return error(&format!("not a length: {length_text}"));
    };
    let Some(material) = workshop::parse_material(material_text) else {
        return error(&format!("unknown material: {material_text}"));
    };
    Output {
        code: 0,
        stdout: format!("{:.2} g\n", workshop::filament_grams(length, material)),
        ..Output::default()
    }
}

fn check_command(material_text: &str, nozzle_text: &str) -> Output {
    let Some(material) = workshop::parse_material(material_text) else {
        return error(&format!("unknown material: {material_text}"));
    };
    let Some(nozzle_c) = workshop::parse_celsius(nozzle_text) else {
        return error(&format!("not a temperature: {nozzle_text}"));
    };

    let verdict = workshop::nozzle_verdict(material, nozzle_c);
    let label = match verdict {
        Verdict::TooCold => "too cold",
        Verdict::Ok => "ok",
        Verdict::TooHot => "too hot",
    };
    let (min, max) = material.nozzle_range();
    Output {
        code: if verdict == Verdict::Ok { 0 } else { 1 },
        stdout: format!("{label}: {} prints at {min}–{max} °C\n", material.name()),
        ..Output::default()
    }
}

fn log_command(path: &Path) -> Output {
    let log = match workshop::load_log(path) {
        Ok(log) => log,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            return error(&format!("no such file: {}", path.display()));
        }
        Err(e) => return error(&format!("could not read {}: {e}", path.display())),
    };

    let mut stdout = format!(
        "entries: {}\nproblems: {}\n",
        log.entries.len(),
        log.problems.len()
    );
    for problem in &log.problems {
        let reason = match problem.error {
            LogLineError::MissingSeparator => "missing separator",
            LogLineError::BadDate => "bad date",
            LogLineError::EmptyText => "empty text",
        };
        stdout.push_str(&format!("  line {}: {reason}\n", problem.line_number));
    }
    Output {
        code: if log.problems.is_empty() { 0 } else { 1 },
        stdout,
        ..Output::default()
    }
}
