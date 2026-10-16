<?php

declare(strict_types=1);

enum Material: string
{
    case PLA = 'PLA';
    case PETG = 'PETG';
    case ABS = 'ABS';
    case TPU = 'TPU';
}

final readonly class Job
{
    public function __construct(
        public string $name,
        public Material $material,
        public float $grams,
    ) {
    }
}

/**
 * @param list<Job> $jobs
 */
function total_grams(array $jobs): float
{
    return array_sum(array_map(fn (Job $job) => $job->grams, $jobs));
}

/**
 * Total grams per material, keyed by the material's value ('PLA', ...).
 *
 * @param list<Job> $jobs
 * @return array<string, float>
 */
function grams_by_material(array $jobs): array
{
    $totals = [];
    foreach ($jobs as $job) {
        $key = $job->material->value;
        $totals[$key] = ($totals[$key] ?? 0.0) + $job->grams;
    }

    return $totals;
}

/**
 * The job with the most grams, or null if there are none. The first wins ties.
 *
 * @param list<Job> $jobs
 */
function heaviest_job(array $jobs): ?Job
{
    $heaviest = null;
    foreach ($jobs as $job) {
        // Strictly greater, so the first of several equal jobs stays.
        if ($heaviest === null || $job->grams > $heaviest->grams) {
            $heaviest = $job;
        }
    }

    return $heaviest;
}

/**
 * Names of the jobs using a material, in their original order.
 *
 * @param list<Job> $jobs
 * @return list<string>
 */
function jobs_using(array $jobs, Material $material): array
{
    $using = array_filter($jobs, fn (Job $job) => $job->material === $material);

    // array_filter keeps the original keys; array_values renumbers from 0.
    return array_values(array_map(fn (Job $job) => $job->name, $using));
}
