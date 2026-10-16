//! Lesson 08: build log.
//!
//! Rust ideas in this lesson: `std::fs`, `std::io::Error` and `?`,
//! `Path`/`PathBuf`, `lines()` and `enumerate()`, and `OpenOptions` for
//! appending.

use std::io;
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
    // TODO: replace this line with your implementation.
    todo!("load_log({path:?})")
}

pub fn append_entry(path: &Path, entry: &LogEntry) -> io::Result<()> {
    // TODO: write the tests in tests/build_log.rs first, then replace this line.
    todo!("append_entry({path:?}, {entry:?})")
}
