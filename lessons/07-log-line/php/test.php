<?php

declare(strict_types=1);

require __DIR__ . '/log.php';

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

// truncate

test('short text is unchanged', function () {
    assert_same('benchy', truncate('benchy', 10));
});

test('text exactly at the limit is unchanged', function () {
    assert_same('1234567890', truncate('1234567890', 10));
});

test('long text is cut and marked', function () {
    assert_same('replaced…', truncate('replaced the nozzle', 8));
});

test('a degree sign counts as one character', function () {
    assert_same('nozzle at 215 °…', truncate('nozzle at 215 °C', 15));
});

test('an emoji counts as one character', function () {
    assert_same('new spool 🧵…', truncate('new spool 🧵 loaded', 11));
});

// format_entry

test('format an entry', function () {
    assert_same('2026-10-16: replaced nozzle', format_entry(new LogEntry('2026-10-16', 'replaced nozzle')));
});

// parse_entry: two examples. Write the error tests before the code.

test('parse a simple line', function () {
    $entry = parse_entry('2026-10-16: replaced nozzle');
    assert_same('2026-10-16', $entry->date);
    assert_same('replaced nozzle', $entry->text);
});

test('parse ignores surrounding spaces', function () {
    $entry = parse_entry('  2026-10-17 :   raised Z offset  ');
    assert_same('2026-10-17', $entry->date);
    assert_same('raised Z offset', $entry->text);
});

test('a colon inside the text is kept', function () {
    assert_same('note: PETG strings', parse_entry('2026-10-18: note: PETG strings')->text);
});

test('format undoes parse', function () {
    $line = '2026-10-18: note: PETG strings above 245 °C';
    assert_same($line, format_entry(parse_entry($line)));
});

test('a line without a colon is missing its separator', function () {
    assert_throws(MissingSeparator::class, fn () => parse_entry('2026-10-16 replaced nozzle'));
});

$badDates = ['16/10/2026', '2026-13-01', '2026-00-10', '2026-10-32', '2026-10-00', '2026-1-5', ''];
foreach ($badDates as $date) {
    test("'{$date}' is a bad date", function () use ($date) {
        assert_throws(BadDate::class, fn () => parse_entry("{$date}: replaced nozzle"));
    });
}

test('blank text is empty', function () {
    assert_throws(EmptyText::class, fn () => parse_entry('2026-10-16:   '));
});

// The tiny test runner reports the result. Nothing to change below this line.
if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
