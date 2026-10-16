//! Lesson 06: batch.
//!
//! Rust ideas in this lesson: slices (`&[Job]`), `Vec`, `HashMap`, iterators
//! and closures, `Option`, and returning references into a collection.
//!
//! `Hash` is derived on `Material` so it can be a `HashMap` key.

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Material {
    Pla,
    Petg,
    Abs,
    Tpu,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Job {
    pub name: String,
    pub material: Material,
    pub grams: f64,
}

pub fn total_grams(jobs: &[Job]) -> f64 {
    // TODO: replace this line with your implementation.
    todo!("total_grams of {} jobs", jobs.len())
}

/// Total grams per material, for the materials that appear.
pub fn grams_by_material(jobs: &[Job]) -> HashMap<Material, f64> {
    todo!("grams_by_material of {} jobs", jobs.len())
}

/// The job with the most grams, or `None` if there are none. The first wins ties.
pub fn heaviest_job(jobs: &[Job]) -> Option<&Job> {
    // TODO: write the tests in tests/batch.rs first, then replace this line.
    todo!("heaviest_job of {} jobs", jobs.len())
}

/// Names of the jobs using a material, in their original order.
pub fn jobs_using(jobs: &[Job], material: Material) -> Vec<&str> {
    todo!("jobs_using {material:?} of {} jobs", jobs.len())
}
