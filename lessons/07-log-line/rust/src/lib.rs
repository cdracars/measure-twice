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
    let (date, text) = line.split_once(':').ok_or(LogLineError::MissingSeparator)?;
    let (date, text) = (date.trim(), text.trim());
    if !is_valid_date(date) {
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

/// Whether a string looks like YYYY-MM-DD. Checks the shape, not the calendar.
fn is_valid_date(date: &str) -> bool {
    let bytes = date.as_bytes();
    let shape_ok = bytes.len() == 10
        && bytes[4] == b'-'
        && bytes[7] == b'-'
        && bytes
            .iter()
            .enumerate()
            .all(|(i, b)| i == 4 || i == 7 || b.is_ascii_digit());
    if !shape_ok {
        return false;
    }
    // Safe to slice: we just checked every byte is ASCII.
    let month: u32 = date[5..7].parse().unwrap_or(0);
    let day: u32 = date[8..10].parse().unwrap_or(0);
    (1..=12).contains(&month) && (1..=31).contains(&day)
}

/// The line for an entry: `"YYYY-MM-DD: text"`.
pub fn format_entry(entry: &LogEntry) -> String {
    format!("{}: {}", entry.date, entry.text)
}

/// The text if it has at most `max_chars` characters, otherwise its first
/// `max_chars` characters followed by `"…"`.
pub fn truncate(text: &str, max_chars: usize) -> String {
    if text.chars().count() <= max_chars {
        return text.to_string();
    }
    let mut short: String = text.chars().take(max_chars).collect();
    short.push('…');
    short
}
