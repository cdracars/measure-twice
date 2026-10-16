<?php

declare(strict_types=1);

require __DIR__ . '/filament.php';

// A tiny test runner, so the lesson needs nothing but PHP itself.
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

function assert_close(float $expected, float $actual, float $tolerance = 0.01): void
{
    if (abs($expected - $actual) > $tolerance) {
        throw new Exception("expected {$expected} (± {$tolerance}), got {$actual}");
    }
}

test('one metre of 1.75 mm PLA weighs about 3 g', function () {
    assert_close(2.98, filament_grams(1000.0, 1.75, 1.24));
});

test('zero length weighs nothing', function () {
    assert_close(0.0, filament_grams(0.0, 1.75, 1.24));
});

test('2.85 mm filament is much heavier per metre', function () {
    assert_close(7.91, filament_grams(1000.0, 2.85, 1.24));
});

test('denser material weighs more (PETG)', function () {
    assert_close(3.05, filament_grams(1000.0, 1.75, 1.27));
});

test('a 1 kg spool of 1.75 mm PLA holds about 335 m', function () {
    assert_close(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), 50.0);
});

test('length and weight convert back and forth', function () {
    $grams = filament_grams(4200.0, 1.75, 1.24);
    assert_close(4200.0, filament_length_mm($grams, 1.75, 1.24));
});

// Your turn: add one test of your own here.

if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
