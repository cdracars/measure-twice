use std::io::ErrorKind;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU32, Ordering};

use lesson_08_build_log::{LogEntry, LogLineError, Problem, append_entry, format_entry, load_log};

fn fixture(name: &str) -> PathBuf {
    // CARGO_MANIFEST_DIR is this crate's folder, set by cargo at build time.
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("fixtures")
        .join(name)
}

/// A new, empty directory that nothing else uses, deleted when the value is
/// dropped (goes out of scope), even if the test panics first. Rust's
/// standard library has no temporary-directory helper, so this builds a
/// unique name from the process id and a counter.
struct TempDir(PathBuf);

impl TempDir {
    fn new() -> TempDir {
        static COUNTER: AtomicU32 = AtomicU32::new(0);
        let n = COUNTER.fetch_add(1, Ordering::SeqCst);
        let dir = std::env::temp_dir().join(format!("measure-twice-{}-{n}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        TempDir(dir)
    }
}

impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

fn entry(date: &str, text: &str) -> LogEntry {
    LogEntry {
        date: date.to_string(),
        text: text.to_string(),
    }
}

fn lines(entries: &[LogEntry]) -> Vec<String> {
    entries.iter().map(format_entry).collect()
}

// load_log

#[test]
fn loads_the_good_entries_in_order() {
    let log = load_log(&fixture("workshop.log")).unwrap();
    assert_eq!(
        lines(&log.entries),
        [
            "2026-10-14: new 0.4 mm nozzle",
            "2026-10-16: replaced PTFE tube",
            "2026-10-18: note: PETG strings above 245 °C",
        ]
    );
}

#[test]
fn reports_each_bad_line_with_its_line_number_and_error() {
    let log = load_log(&fixture("workshop.log")).unwrap();
    assert_eq!(
        log.problems,
        [
            Problem {
                line_number: 4,
                error: LogLineError::MissingSeparator
            },
            Problem {
                line_number: 6,
                error: LogLineError::BadDate
            },
            Problem {
                line_number: 7,
                error: LogLineError::EmptyText
            },
        ]
    );
}

#[test]
fn an_empty_file_has_no_entries_and_no_problems() {
    let log = load_log(&fixture("empty.log")).unwrap();
    assert!(log.entries.is_empty());
    assert!(log.problems.is_empty());
}

#[test]
fn windows_line_endings_are_handled() {
    let log = load_log(&fixture("windows.log")).unwrap();
    let texts: Vec<&str> = log.entries.iter().map(|e| e.text.as_str()).collect();
    assert_eq!(texts, ["new nozzle", "dried PETG"]);
}

#[test]
fn a_missing_file_is_reported() {
    let error = load_log(&fixture("no-such-file.log")).unwrap_err();
    assert_eq!(error.kind(), ErrorKind::NotFound);
}

// append_entry: one example. Write the rest before the code.

#[test]
fn appending_to_a_new_file_creates_it() {
    let dir = TempDir::new();
    let path = dir.0.join("build.log");
    append_entry(&path, &entry("2026-10-19", "levelled the bed")).unwrap();
    assert_eq!(
        lines(&load_log(&path).unwrap().entries),
        ["2026-10-19: levelled the bed"]
    );
}
