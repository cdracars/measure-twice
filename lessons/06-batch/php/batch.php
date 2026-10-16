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
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement total_grams');
}

/**
 * Total grams per material, keyed by the material's value ('PLA', ...).
 *
 * @param list<Job> $jobs
 * @return array<string, float>
 */
function grams_by_material(array $jobs): array
{
    throw new RuntimeException('TODO: implement grams_by_material');
}

/**
 * The job with the most grams, or null if there are none. The first wins ties.
 *
 * @param list<Job> $jobs
 */
function heaviest_job(array $jobs): ?Job
{
    // TODO: write the tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement heaviest_job');
}

/**
 * Names of the jobs using a material, in their original order.
 *
 * @param list<Job> $jobs
 * @return list<string>
 */
function jobs_using(array $jobs, Material $material): array
{
    throw new RuntimeException('TODO: implement jobs_using');
}
