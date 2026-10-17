<?php

declare(strict_types=1);

require __DIR__ . '/temperature.php';

// The same tiny test runner as lesson 01.
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

// nozzle_verdict

test('PLA in the middle of its range is ok', function () {
    assert_same('ok', nozzle_verdict('PLA', 205));
});

test('PLA at its minimum is ok', function () {
    assert_same('ok', nozzle_verdict('PLA', 190));
});

test('PLA one degree below its minimum is too cold', function () {
    assert_same('too cold', nozzle_verdict('PLA', 189));
});

test('PLA at its maximum is ok', function () {
    assert_same('ok', nozzle_verdict('PLA', 220));
});

test('PLA one degree above its maximum is too hot', function () {
    assert_same('too hot', nozzle_verdict('PLA', 221));
});

test('PETG at a PLA temperature is too cold', function () {
    assert_same('too cold', nozzle_verdict('PETG', 200));
});

test('ABS at its maximum is ok', function () {
    assert_same('ok', nozzle_verdict('ABS', 260));
});

test('TPU above its maximum is too hot', function () {
    assert_same('too hot', nozzle_verdict('TPU', 231));
});

test('an unknown material is reported', function () {
    assert_same('unknown material', nozzle_verdict('Nylon', 250));
});

test('material names are exact', function () {
    assert_same('unknown material', nozzle_verdict('pla', 205));
});

// needs_enclosure: one example. Write the rest before the code.

test('ABS needs an enclosure', function () {
    assert_same(true, needs_enclosure('ABS'));
});

test('PLA does not need an enclosure', function () {
    assert_same(false, needs_enclosure('PLA'));
});

test('PETG does not need an enclosure', function () {
    assert_same(false, needs_enclosure('PETG'));
});

test('TPU does not need an enclosure', function () {
    assert_same(false, needs_enclosure('TPU'));
});

test('an unknown material does not need an enclosure', function () {
    assert_same(false, needs_enclosure('Nylon'));
});

// The tiny test runner reports the result. Nothing to change below this line.
if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
