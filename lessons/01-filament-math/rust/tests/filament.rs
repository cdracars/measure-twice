use lesson_01_filament_math::{filament_grams, filament_length_mm};

// #[track_caller]: when this fails, report the line of the test that called
// it, not a line inside this helper.
#[track_caller]
fn assert_close(expected: f64, actual: f64, tolerance: f64) {
    assert!(
        (expected - actual).abs() <= tolerance,
        "expected {expected} (± {tolerance}), got {actual}"
    );
}

#[test]
fn one_metre_of_pla_weighs_about_3_g() {
    assert_close(2.98, filament_grams(1000.0, 1.75, 1.24), 0.01);
}

#[test]
fn zero_length_weighs_nothing() {
    assert_close(0.0, filament_grams(0.0, 1.75, 1.24), 0.01);
}

#[test]
fn thicker_filament_is_much_heavier_per_metre() {
    assert_close(7.91, filament_grams(1000.0, 2.85, 1.24), 0.01);
}

#[test]
fn denser_material_weighs_more() {
    assert_close(3.05, filament_grams(1000.0, 1.75, 1.27), 0.01);
}

#[test]
fn a_1_kg_spool_holds_about_335_m() {
    assert_close(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), 50.0);
}

#[test]
fn length_and_weight_convert_back_and_forth() {
    let grams = filament_grams(4200.0, 1.75, 1.24);
    assert_close(4200.0, filament_length_mm(grams, 1.75, 1.24), 0.01);
}

// Last step of this lesson: add one test of your own here. The guide tells you when.

#[test]
fn one_metre_of_tpu_weighs_about_2_91_g() {
    assert_close(2.91, filament_grams(1000.0, 1.75, 1.21), 0.01);
}
