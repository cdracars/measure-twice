//! Lesson 07: log line.
//!
//! Rust ideas in this lesson: `String` vs `&str`, `split_once`, `trim`,
//! `chars()`, `format!`, and why byte slicing can panic.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LogEntry {
    pub date: String,
    pub text: String,
}

// The errors. They're given: your job is to return them.

/// Every way a log line can be invalid.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLineError {
    MissingSeparator,
    BadDate,
    EmptyText,
}

/// A log entry from a line like `"2026-10-16: replaced nozzle"`.
pub fn parse_entry(line: &str) -> Result<LogEntry, LogLineError> {
    // TODO: write the error tests in tests/log.rs first, then replace this line.
    todo!("parse_entry({line:?})")
}

/// The line for an entry: `"YYYY-MM-DD: text"`.
pub fn format_entry(entry: &LogEntry) -> String {
    // TODO: replace this line with your implementation.
    todo!("format_entry({entry:?})")
}

/// The text if it has at most `max_chars` characters, otherwise its first
/// `max_chars` characters followed by `"…"`.
pub fn truncate(text: &str, max_chars: usize) -> String {
    todo!("truncate({text:?}, {max_chars})")
}
