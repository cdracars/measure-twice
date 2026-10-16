<?php

declare(strict_types=1);

require __DIR__ . '/batch.php';

// The same tiny test runner as earlier lessons.
$failures = 0;

function test(string $name, callable $body): void
{
    global $failures;
    try {
        $body();
        echo "  ok    {$name}\n";
    } catch (Throwable $e) {
        $failures++;
        echo "  FAIL  {$name}\n        {$e->getMessage()}\n";
    }
}

function assert_same(mixed $expected, mixed $actual): void
{
    if ($expected !== $actual) {
        $e = var_export($expected, true);
        $a = var_export($actual, true);
        throw new Exception("expected {$e}, got {$a}");
    }
}

/**
 * @return list<Job>
 */
function friday_queue(): array
{
    return [
        new Job('benchy', Material::PLA, 12.5),
        new Job('bracket', Material::PETG, 40.0),
        new Job('phone case', Material::TPU, 22.25),
        new Job('vase', Material::PLA, 85.0),
        new Job('enclosure hinge', Material::ABS, 7.75),
    ];
}

test('total grams of a batch', function () {
    assert_same(167.5, total_grams(friday_queue()));
});

test('total grams of no jobs is zero', function () {
    assert_same(0.0, total_grams([]));
});

test('grams by material', function () {
    $byMaterial = grams_by_material(friday_queue());
    ksort($byMaterial);
    assert_same(['ABS' => 7.75, 'PETG' => 40.0, 'PLA' => 97.5, 'TPU' => 22.25], $byMaterial);
});

test('grams by material leaves out materials that are not used', function () {
    $jobs = [new Job('benchy', Material::PLA, 12.5)];
    assert_same(['PLA' => 12.5], grams_by_material($jobs));
});

test('jobs using PLA, in order', function () {
    assert_same(['benchy', 'vase'], jobs_using(friday_queue(), Material::PLA));
});

test('jobs using a material nobody uses', function () {
    $jobs = [new Job('benchy', Material::PLA, 12.5)];
    assert_same([], jobs_using($jobs, Material::ABS));
});

// heaviest_job: one example. Write the tricky cases before the code.

test('the heaviest job in the batch', function () {
    assert_same('vase', heaviest_job(friday_queue())?->name);
});

if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
