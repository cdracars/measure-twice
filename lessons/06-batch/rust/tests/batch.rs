use std::collections::HashMap;

use lesson_06_batch::{Job, Material, grams_by_material, heaviest_job, jobs_using, total_grams};

fn job(name: &str, material: Material, grams: f64) -> Job {
    Job {
        name: name.to_string(),
        material,
        grams,
    }
}

fn friday_queue() -> Vec<Job> {
    vec![
        job("benchy", Material::Pla, 12.5),
        job("bracket", Material::Petg, 40.0),
        job("phone case", Material::Tpu, 22.25),
        job("vase", Material::Pla, 85.0),
        job("enclosure hinge", Material::Abs, 7.75),
    ]
}

#[test]
fn total_grams_of_a_batch() {
    assert_eq!(total_grams(&friday_queue()), 167.5);
}

#[test]
fn total_grams_of_no_jobs_is_zero() {
    assert_eq!(total_grams(&[]), 0.0);
}

#[test]
fn grams_by_material_of_a_batch() {
    let expected = HashMap::from([
        (Material::Pla, 97.5),
        (Material::Petg, 40.0),
        (Material::Tpu, 22.25),
        (Material::Abs, 7.75),
    ]);
    assert_eq!(grams_by_material(&friday_queue()), expected);
}

#[test]
fn grams_by_material_leaves_out_materials_that_are_not_used() {
    let jobs = [job("benchy", Material::Pla, 12.5)];
    assert_eq!(
        grams_by_material(&jobs),
        HashMap::from([(Material::Pla, 12.5)])
    );
}

#[test]
fn jobs_using_pla_in_order() {
    assert_eq!(
        jobs_using(&friday_queue(), Material::Pla),
        vec!["benchy", "vase"]
    );
}

#[test]
fn jobs_using_a_material_nobody_uses() {
    let jobs = [job("benchy", Material::Pla, 12.5)];
    assert!(jobs_using(&jobs, Material::Abs).is_empty());
}

// heaviest_job: one example. Write the tricky cases before the code.

#[test]
fn the_heaviest_job_in_the_batch() {
    let jobs = friday_queue();
    assert_eq!(heaviest_job(&jobs).map(|j| j.name.as_str()), Some("vase"));
}

#[test]
fn no_jobs_means_no_heaviest_job() {
    assert_eq!(heaviest_job(&[]), None);
}

#[test]
fn the_first_of_two_equally_heavy_jobs_wins() {
    let jobs = [
        job("left bracket", Material::Petg, 40.0),
        job("right bracket", Material::Petg, 40.0),
    ];
    assert_eq!(
        heaviest_job(&jobs).map(|j| j.name.as_str()),
        Some("left bracket")
    );
}
