<?php

declare(strict_types=1);

require __DIR__ . '/Spool.php';

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

function assert_close(float $expected, float $actual, float $tolerance = 0.01): void
{
    if (abs($expected - $actual) > $tolerance) {
        throw new Exception("expected {$expected} (± {$tolerance}), got {$actual}");
    }
}

function full_pla_spool(): Spool
{
    return new Spool('PLA', 1.75, 1.24, 1000.0);
}

test('a new spool knows its material', function () {
    assert_same('PLA', full_pla_spool()->material());
});

test('a new spool knows how much is left', function () {
    assert_close(1000.0, full_pla_spool()->gramsRemaining());
});

test('a full 1 kg PLA spool holds about 335 m', function () {
    assert_close(335_280.0, full_pla_spool()->remainingLengthMm(), 50.0);
});

test('a half-used spool holds half the length', function () {
    $spool = new Spool('PLA', 1.75, 1.24, 500.0);
    assert_close(167_640.0, $spool->remainingLengthMm(), 50.0);
});

test('a small job can print', function () {
    assert_same(true, full_pla_spool()->canPrint(25.0));
});

test('a job needing exactly what is left can print', function () {
    assert_same(true, full_pla_spool()->canPrint(1000.0));
});

test('a job needing more than is left cannot print', function () {
    assert_same(false, full_pla_spool()->canPrint(1000.1));
});

test('remaining grams cannot be set from outside', function () {
    $property = new ReflectionProperty(Spool::class, 'gramsRemaining');
    assert_same(true, $property->isPrivate());
});

// consume: no tests yet. Write them before the code.

// The tiny test runner reports the result. Nothing to change below this line.
if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
