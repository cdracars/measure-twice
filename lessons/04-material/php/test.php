<?php

declare(strict_types=1);

require __DIR__ . '/material.php';

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

function assert_close(float $expected, float $actual, float $tolerance = 0.001): void
{
    if (abs($expected - $actual) > $tolerance) {
        throw new Exception("expected {$expected} (± {$tolerance}), got {$actual}");
    }
}

test('PLA density', fn () => assert_close(1.24, Material::PLA->density()));
test('PETG density', fn () => assert_close(1.27, Material::PETG->density()));
test('ABS density', fn () => assert_close(1.04, Material::ABS->density()));
test('TPU density', fn () => assert_close(1.21, Material::TPU->density()));

test('PLA nozzle range', function () {
    assert_same([190, 220], Material::PLA->nozzleRange());
});

test('every nozzle range runs from low to high', function () {
    foreach (Material::cases() as $material) {
        [$min, $max] = $material->nozzleRange();
        if ($min >= $max) {
            throw new Exception("{$material->name}: {$min} is not below {$max}");
        }
    }
});

test('ABS needs an enclosure', function () {
    assert_same(true, Material::ABS->needsEnclosure());
});

test('no other material needs an enclosure', function () {
    foreach (Material::cases() as $material) {
        if ($material !== Material::ABS) {
            assert_same(false, $material->needsEnclosure());
        }
    }
});

// nozzle_verdict: one example. Write the boundary tests before the code.

test('PLA in the middle of its range is OK', function () {
    assert_same(Verdict::Ok, nozzle_verdict(Material::PLA, 205));
});

$boundaries = [
    [Material::PLA, 189, Verdict::TooCold],
    [Material::PLA, 190, Verdict::Ok],
    [Material::PLA, 220, Verdict::Ok],
    [Material::PLA, 221, Verdict::TooHot],
    [Material::ABS, 229, Verdict::TooCold],
    [Material::ABS, 230, Verdict::Ok],
    [Material::ABS, 260, Verdict::Ok],
    [Material::ABS, 261, Verdict::TooHot],
];
foreach ($boundaries as [$material, $nozzleC, $expected]) {
    test("{$material->name} at {$nozzleC} °C is {$expected->name}", function () use ($material, $nozzleC, $expected) {
        assert_same($expected, nozzle_verdict($material, $nozzleC));
    });
}

// The tiny test runner reports the result. Nothing to change below this line.
if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
