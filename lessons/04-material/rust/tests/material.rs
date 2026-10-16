use lesson_04_material::{Material, Verdict, nozzle_verdict};

fn assert_close(expected: f64, actual: f64) {
    assert!(
        (expected - actual).abs() <= 0.001,
        "expected {expected}, got {actual}"
    );
}

#[test]
fn densities() {
    assert_close(1.24, Material::Pla.density());
    assert_close(1.27, Material::Petg.density());
    assert_close(1.04, Material::Abs.density());
    assert_close(1.21, Material::Tpu.density());
}

#[test]
fn pla_nozzle_range() {
    assert_eq!(Material::Pla.nozzle_range(), (190, 220));
}

#[test]
fn every_nozzle_range_runs_from_low_to_high() {
    for material in Material::ALL {
        let (min, max) = material.nozzle_range();
        assert!(min < max, "{material:?}: {min} is not below {max}");
    }
}

#[test]
fn abs_needs_an_enclosure() {
    assert!(Material::Abs.needs_enclosure());
}

#[test]
fn no_other_material_needs_an_enclosure() {
    for material in Material::ALL {
        if material != Material::Abs {
            assert!(!material.needs_enclosure(), "{material:?}");
        }
    }
}

// nozzle_verdict: one example. Write the boundary tests before the code.

#[test]
fn pla_in_the_middle_of_its_range_is_ok() {
    assert_eq!(nozzle_verdict(Material::Pla, 205), Verdict::Ok);
}
