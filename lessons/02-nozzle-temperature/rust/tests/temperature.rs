use lesson_02_nozzle_temperature::{needs_enclosure, nozzle_verdict};

// nozzle_verdict

#[test]
fn pla_in_the_middle_of_its_range_is_ok() {
    assert_eq!(nozzle_verdict("PLA", 205), "ok");
}

#[test]
fn pla_at_its_minimum_is_ok() {
    assert_eq!(nozzle_verdict("PLA", 190), "ok");
}

#[test]
fn pla_one_degree_below_its_minimum_is_too_cold() {
    assert_eq!(nozzle_verdict("PLA", 189), "too cold");
}

#[test]
fn pla_at_its_maximum_is_ok() {
    assert_eq!(nozzle_verdict("PLA", 220), "ok");
}

#[test]
fn pla_one_degree_above_its_maximum_is_too_hot() {
    assert_eq!(nozzle_verdict("PLA", 221), "too hot");
}

#[test]
fn petg_at_a_pla_temperature_is_too_cold() {
    assert_eq!(nozzle_verdict("PETG", 200), "too cold");
}

#[test]
fn abs_at_its_maximum_is_ok() {
    assert_eq!(nozzle_verdict("ABS", 260), "ok");
}

#[test]
fn tpu_above_its_maximum_is_too_hot() {
    assert_eq!(nozzle_verdict("TPU", 231), "too hot");
}

#[test]
fn an_unknown_material_is_reported() {
    assert_eq!(nozzle_verdict("Nylon", 250), "unknown material");
}

#[test]
fn material_names_are_exact() {
    assert_eq!(nozzle_verdict("pla", 205), "unknown material");
}

// needs_enclosure: one example. Write the rest before the code.

#[test]
fn abs_needs_an_enclosure() {
    assert!(needs_enclosure("ABS"));
}
