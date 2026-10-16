use lesson_03_spool::Spool;

fn assert_close(expected: f64, actual: f64, tolerance: f64) {
    assert!(
        (expected - actual).abs() <= tolerance,
        "expected {expected} (± {tolerance}), got {actual}"
    );
}

fn full_pla_spool() -> Spool {
    Spool::new("PLA", 1.75, 1.24, 1000.0)
}

#[test]
fn a_new_spool_knows_its_material() {
    assert_eq!(full_pla_spool().material(), "PLA");
}

#[test]
fn a_new_spool_knows_how_much_is_left() {
    assert_close(1000.0, full_pla_spool().grams_remaining(), 0.01);
}

#[test]
fn a_full_1_kg_pla_spool_holds_about_335_m() {
    assert_close(335_280.0, full_pla_spool().remaining_length_mm(), 50.0);
}

#[test]
fn a_half_used_spool_holds_half_the_length() {
    let spool = Spool::new("PLA", 1.75, 1.24, 500.0);
    assert_close(167_640.0, spool.remaining_length_mm(), 50.0);
}

#[test]
fn a_small_job_can_print() {
    assert!(full_pla_spool().can_print(25.0));
}

#[test]
fn a_job_needing_exactly_what_is_left_can_print() {
    assert!(full_pla_spool().can_print(1000.0));
}

#[test]
fn a_job_needing_more_than_is_left_cannot_print() {
    assert!(!full_pla_spool().can_print(1000.1));
}

// There's no test that the fields are private: in Rust, code that tried to
// write `spool.grams_remaining = 5000.0` from here wouldn't compile at all.
// Try it.

// consume: no tests yet. Write them before the code. Remember `let mut`.

#[test]
fn consuming_reduces_what_is_left() {
    let mut spool = full_pla_spool();
    spool.consume(250.0);
    assert_close(750.0, spool.grams_remaining(), 0.01);
}

#[test]
fn two_jobs_in_a_row_add_up() {
    let mut spool = full_pla_spool();
    spool.consume(100.0);
    spool.consume(50.0);
    assert_close(850.0, spool.grams_remaining(), 0.01);
}

#[test]
fn consuming_everything_leaves_nothing_to_print_with() {
    let mut spool = full_pla_spool();
    spool.consume(1000.0);
    assert_close(0.0, spool.grams_remaining(), 0.01);
    assert!(!spool.can_print(0.1));
}

#[test]
fn consuming_shortens_the_remaining_length() {
    let mut spool = full_pla_spool();
    spool.consume(500.0);
    assert_close(167_640.0, spool.remaining_length_mm(), 50.0);
}
