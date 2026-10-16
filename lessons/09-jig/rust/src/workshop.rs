//! Finished pieces from lessons 01–08. You don't need to change this file.

use std::f64::consts::PI;
use std::fs;
use std::io;
use std::path::Path;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Material {
    Pla,
    Petg,
    Abs,
    Tpu,
}

impl Material {
    /// The material's name in capitals, as users type it: `"PLA"`.
    pub fn name(self) -> &'static str {
        match self {
            Material::Pla => "PLA",
            Material::Petg => "PETG",
            Material::Abs => "ABS",
            Material::Tpu => "TPU",
        }
    }

    pub fn density(self) -> f64 {
        match self {
            Material::Pla => 1.24,
            Material::Petg => 1.27,
            Material::Abs => 1.04,
            Material::Tpu => 1.21,
        }
    }

    pub fn nozzle_range(self) -> (i32, i32) {
        match self {
            Material::Pla => (190, 220),
            Material::Petg => (220, 250),
            Material::Abs => (230, 260),
            Material::Tpu => (210, 230),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    TooCold,
    Ok,
    TooHot,
}

/// The material, or `None` if the text isn't one. Ignores case and spaces.
pub fn parse_material(text: &str) -> Option<Material> {
    match text.trim().to_ascii_uppercase().as_str() {
        "PLA" => Some(Material::Pla),
        "PETG" => Some(Material::Petg),
        "ABS" => Some(Material::Abs),
        "TPU" => Some(Material::Tpu),
        _ => None,
    }
}

/// A length in mm such as `"1000"` or `"12.5"`, or `None` if the text isn't one.
pub fn parse_length_mm(text: &str) -> Option<f64> {
    let text = text.trim();
    let (whole, fraction) = text.split_once('.').unwrap_or((text, "0"));
    let digits = |s: &str| !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit());
    if digits(whole) && digits(fraction) {
        text.parse().ok()
    } else {
        None
    }
}

/// A whole number of °C such as `"205"`, or `None` if the text isn't one.
pub fn parse_celsius(text: &str) -> Option<i32> {
    text.trim().parse().ok()
}

/// Weight in grams of a length of 1.75 mm filament.
pub fn filament_grams(length_mm: f64, material: Material) -> f64 {
    let area_mm2 = PI * (1.75_f64 / 2.0).powi(2);
    length_mm * area_mm2 / 1000.0 * material.density()
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

// The Build Log, from lessons 07 and 08.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LogEntry {
    pub date: String,
    pub text: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLineError {
    MissingSeparator,
    BadDate,
    EmptyText,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Problem {
    pub line_number: usize,
    pub error: LogLineError,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LoadedLog {
    pub entries: Vec<LogEntry>,
    pub problems: Vec<Problem>,
}

pub fn parse_entry(line: &str) -> Result<LogEntry, LogLineError> {
    let (date, text) = line.split_once(':').ok_or(LogLineError::MissingSeparator)?;
    let (date, text) = (date.trim(), text.trim());
    let b = date.as_bytes();
    let shape_ok = b.len() == 10
        && b.iter().enumerate().all(|(i, c)| {
            if i == 4 || i == 7 {
                *c == b'-'
            } else {
                c.is_ascii_digit()
            }
        });
    let month: u32 = if shape_ok {
        date[5..7].parse().unwrap_or(0)
    } else {
        0
    };
    let day: u32 = if shape_ok {
        date[8..10].parse().unwrap_or(0)
    } else {
        0
    };
    if !(1..=12).contains(&month) || !(1..=31).contains(&day) {
        return Err(LogLineError::BadDate);
    }
    if text.is_empty() {
        return Err(LogLineError::EmptyText);
    }
    Ok(LogEntry {
        date: date.to_string(),
        text: text.to_string(),
    })
}

/// Errors with `kind()` `NotFound` if the file doesn't exist.
pub fn load_log(path: &Path) -> io::Result<LoadedLog> {
    let text = fs::read_to_string(path)?;
    let mut entries = Vec::new();
    let mut problems = Vec::new();
    for (index, line) in text.lines().enumerate() {
        let trimmed = line.trim();
        if trimmed.is_empty() || trimmed.starts_with('#') {
            continue;
        }
        match parse_entry(line) {
            Ok(entry) => entries.push(entry),
            Err(error) => problems.push(Problem {
                line_number: index + 1,
                error,
            }),
        }
    }
    Ok(LoadedLog { entries, problems })
}
