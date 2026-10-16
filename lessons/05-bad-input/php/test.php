<?php

declare(strict_types=1);

require __DIR__ . '/parse.php';

// The same tiny test runner as earlier lessons, plus assert_throws.
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
 * @param class-string<Throwable> $class
 */
function assert_throws(string $class, callable $body): void
{
    try {
        $body();
    } catch (Throwable $e) {
        if ($e instanceof $class) {
            return;
        }
        throw new Exception("expected {$class}, got " . $e::class . ": {$e->getMessage()}");
    }
    throw new Exception("expected {$class}, but nothing was thrown");
}

// parse_grams: accepted

$accepted = [
    '250' => 250.0,
    '12.5' => 12.5,
    '12.5 g' => 12.5,
    '40g' => 40.0,
    ' 40g ' => 40.0,
    '0' => 0.0,
];
foreach ($accepted as $text => $grams) {
    test("parse_grams accepts '{$text}'", function () use ($text, $grams) {
        assert_same($grams, parse_grams((string) $text));
    });
}

// parse_grams: rejected

$rejected = [
    '' => EmptyInput::class,
    '   ' => EmptyInput::class,
    'abc' => NotANumber::class,
    '12.5 kg' => NotANumber::class,
    'nan' => NotANumber::class,
    'inf' => NotANumber::class,
    '0x10' => NotANumber::class,
    '1_000' => NotANumber::class,
    '-5' => NegativeAmount::class,
    '-5 g' => NegativeAmount::class,
];
foreach ($rejected as $text => $error) {
    test("parse_grams rejects '{$text}' as {$error}", function () use ($text, $error) {
        assert_throws($error, fn () => parse_grams((string) $text));
    });
}

test('every grams error can be caught as InvalidAmount', function () {
    assert_throws(InvalidAmount::class, fn () => parse_grams('abc'));
});

// Spool::consume

test('consuming what is available works', function () {
    $spool = new Spool(100.0);
    $spool->consume(40.0);
    assert_same(60.0, $spool->gramsRemaining());
});

test('consuming exactly what is left works', function () {
    $spool = new Spool(100.0);
    $spool->consume(100.0);
    assert_same(0.0, $spool->gramsRemaining());
});

test('consuming more than is left is refused', function () {
    $spool = new Spool(100.0);
    assert_throws(NotEnoughFilament::class, fn () => $spool->consume(100.5));
});

test('a refused consume leaves the spool unchanged', function () {
    $spool = new Spool(100.0);
    try {
        $spool->consume(150.0);
    } catch (NotEnoughFilament) {
        // expected
    }
    assert_same(100.0, $spool->gramsRemaining());
});

// parse_material: one example. Write the rest before the code.

test('parse_material accepts PLA', function () {
    assert_same(Material::PLA, parse_material('PLA'));
});

if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
