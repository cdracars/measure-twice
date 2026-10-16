<?php

declare(strict_types=1);

require __DIR__ . '/cli.php';

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

function assert_output(Output $expected, Output $actual): void
{
    assert_same(
        [$expected->code, $expected->stdout, $expected->stderr],
        [$actual->code, $actual->stdout, $actual->stderr],
    );
}

// help and errors

test('help prints the usage', function () {
    assert_output(new Output(0, stdout: USAGE), run(['help']));
});

test('no arguments prints the usage as an error', function () {
    assert_output(new Output(2, stderr: USAGE), run([]));
});

test('an unknown command is an error', function () {
    assert_output(
        new Output(2, stderr: "jig: unknown command: frobnicate\nrun 'jig help' to see the commands\n"),
        run(['frobnicate']),
    );
});

// grams

test('grams of PLA', function () {
    assert_output(new Output(0, stdout: "2.98 g\n"), run(['grams', '1000', 'PLA']));
});

test('grams accepts a lowercase material', function () {
    assert_output(new Output(0, stdout: "12.83 g\n"), run(['grams', '4200', 'petg']));
});

test('grams rejects a bad length', function () {
    assert_output(new Output(2, stderr: "jig: not a length: abc\n"), run(['grams', 'abc', 'PLA']));
});

test('grams rejects an unknown material', function () {
    assert_output(new Output(2, stderr: "jig: unknown material: Nylon\n"), run(['grams', '1000', 'Nylon']));
});

test('grams needs exactly two arguments', function () {
    assert_output(
        new Output(2, stderr: "jig: usage: jig grams <length-mm> <material>\n"),
        run(['grams', '1000']),
    );
});

// check

test('check a good temperature', function () {
    assert_output(new Output(0, stdout: "ok: PLA prints at 190–220 °C\n"), run(['check', 'PLA', '205']));
});

test('check a cold temperature', function () {
    assert_output(new Output(1, stdout: "too cold: PETG prints at 220–250 °C\n"), run(['check', 'petg', '200']));
});

test('check a hot temperature', function () {
    assert_output(new Output(1, stdout: "too hot: TPU prints at 210–230 °C\n"), run(['check', 'TPU', '240']));
});

test('check rejects a bad temperature', function () {
    assert_output(new Output(2, stderr: "jig: not a temperature: hot\n"), run(['check', 'PLA', 'hot']));
});

test('check needs exactly two arguments', function () {
    assert_output(
        new Output(2, stderr: "jig: usage: jig check <material> <nozzle-c>\n"),
        run(['check', 'PLA', '205', 'extra']),
    );
});

// log: no tests yet. Write them before the code.

if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
