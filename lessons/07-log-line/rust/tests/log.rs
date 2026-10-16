use lesson_07_log_line::{LogEntry, format_entry, parse_entry, truncate};

fn entry(date: &str, text: &str) -> LogEntry {
    LogEntry {
        date: date.to_string(),
        text: text.to_string(),
    }
}

// truncate

#[test]
fn short_text_is_unchanged() {
    assert_eq!(truncate("benchy", 10), "benchy");
}

#[test]
fn text_exactly_at_the_limit_is_unchanged() {
    assert_eq!(truncate("1234567890", 10), "1234567890");
}

#[test]
fn long_text_is_cut_and_marked() {
    assert_eq!(truncate("replaced the nozzle", 8), "replaced…");
}

#[test]
fn a_degree_sign_counts_as_one_character() {
    assert_eq!(truncate("nozzle at 215 °C", 15), "nozzle at 215 °…");
}

#[test]
fn an_emoji_counts_as_one_character() {
    assert_eq!(truncate("new spool 🧵 loaded", 11), "new spool 🧵…");
}

// format_entry

#[test]
fn format_an_entry() {
    assert_eq!(
        format_entry(&entry("2026-10-16", "replaced nozzle")),
        "2026-10-16: replaced nozzle"
    );
}

// parse_entry: two examples. Write the error tests before the code.

#[test]
fn parse_a_simple_line() {
    assert_eq!(
        parse_entry("2026-10-16: replaced nozzle"),
        Ok(entry("2026-10-16", "replaced nozzle"))
    );
}

#[test]
fn parse_ignores_surrounding_spaces() {
    assert_eq!(
        parse_entry("  2026-10-17 :   raised Z offset  "),
        Ok(entry("2026-10-17", "raised Z offset"))
    );
}
