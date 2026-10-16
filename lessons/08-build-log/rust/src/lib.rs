//! Lesson 08: build log.
//!
//! Rust ideas in this lesson: `std::fs`, `std::io::Error` and `?`,
//! `Path`/`PathBuf`, `lines()` and `enumerate()`, and `OpenOptions` for
//! appending.

use std::fs::{self, OpenOptions};
use std::io::{self, Write};
use std::path::Path;

// From lesson 07, finished.

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

pub fn format_entry(entry: &LogEntry) -> String {
    format!("{}: {}", entry.date, entry.text)
}

// New in this lesson.

/// One bad line in a log file.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Problem {
    pub line_number: usize,
    pub error: LogLineError,
}

/// Everything read from a log file: the good entries and the bad lines.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LoadedLog {
    pub entries: Vec<LogEntry>,
    pub problems: Vec<Problem>,
}

pub fn load_log(path: &Path) -> io::Result<LoadedLog> {
    let text = fs::read_to_string(path)?;
    let mut entries = Vec::new();
    let mut problems = Vec::new();
    // `lines()` handles both "\n" and "\r\n".
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

pub fn append_entry(path: &Path, entry: &LogEntry) -> io::Result<()> {
    let mut file = OpenOptions::new().create(true).append(true).open(path)?;
    writeln!(file, "{}", format_entry(entry))
}
