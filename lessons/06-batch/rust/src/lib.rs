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
    jobs.iter().map(|job| job.grams).sum()
}

/// Total grams per material, for the materials that appear.
pub fn grams_by_material(jobs: &[Job]) -> HashMap<Material, f64> {
    let mut totals = HashMap::new();
    for job in jobs {
        *totals.entry(job.material).or_insert(0.0) += job.grams;
    }
    totals
}

/// The job with the most grams, or `None` if there are none. The first wins ties.
pub fn heaviest_job(jobs: &[Job]) -> Option<&Job> {
    // Not `max_by`: it returns the *last* of several equal items.
    let mut heaviest: Option<&Job> = None;
    for job in jobs {
        if heaviest.is_none_or(|h| job.grams > h.grams) {
            heaviest = Some(job);
        }
    }
    heaviest
}

/// Names of the jobs using a material, in their original order.
pub fn jobs_using(jobs: &[Job], material: Material) -> Vec<&str> {
    jobs.iter()
        .filter(|job| job.material == material)
        .map(|job| job.name.as_str())
        .collect()
}
