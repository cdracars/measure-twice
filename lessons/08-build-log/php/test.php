<?php

declare(strict_types=1);

require __DIR__ . '/build_log.php';

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

function fixture(string $name): string
{
    return __DIR__ . "/../fixtures/{$name}";
}

/** A new, empty directory that nothing else uses, deleted when the tests end. */
function fresh_temp_dir(): string
{
    $dir = sys_get_temp_dir() . '/measure-twice-' . bin2hex(random_bytes(8));
    mkdir($dir);
    register_shutdown_function(function () use ($dir) {
        foreach (glob("{$dir}/*") ?: [] as $file) {
            unlink($file);
        }
        rmdir($dir);
    });

    return $dir;
}

/**
 * @param list<LogEntry> $entries
 * @return list<string>
 */
function lines(array $entries): array
{
    return array_map('format_entry', $entries);
}

// load_log

test('loads the good entries in order', function () {
    assert_same([
        '2026-10-14: new 0.4 mm nozzle',
        '2026-10-16: replaced PTFE tube',
        '2026-10-18: note: PETG strings above 245 °C',
    ], lines(load_log(fixture('workshop.log'))->entries));
});

test('reports each bad line with its line number and error', function () {
    $problems = load_log(fixture('workshop.log'))->problems;
    assert_same([4, 6, 7], array_map(fn (Problem $p) => $p->lineNumber, $problems));
    assert_same(
        [MissingSeparator::class, BadDate::class, EmptyText::class],
        array_map(fn (Problem $p) => $p->error::class, $problems),
    );
});

test('an empty file has no entries and no problems', function () {
    $log = load_log(fixture('empty.log'));
    assert_same([], $log->entries);
    assert_same([], $log->problems);
});

test('Windows line endings are handled', function () {
    $entries = load_log(fixture('windows.log'))->entries;
    assert_same(['new nozzle', 'dried PETG'], array_map(fn (LogEntry $e) => $e->text, $entries));
});

test('a missing file is reported', function () {
    assert_throws(LogFileNotFound::class, fn () => load_log(fixture('no-such-file.log')));
});

// append_entry: one example. Write the rest before the code.

test('appending to a new file creates it', function () {
    $path = fresh_temp_dir() . '/build.log';
    append_entry($path, new LogEntry('2026-10-19', 'levelled the bed'));
    assert_same(['2026-10-19: levelled the bed'], lines(load_log($path)->entries));
});

test('appending twice keeps the order', function () {
    $path = fresh_temp_dir() . '/build.log';
    append_entry($path, new LogEntry('2026-10-19', 'levelled the bed'));
    append_entry($path, new LogEntry('2026-10-20', 'printed a calibration cube'));
    assert_same(
        ['2026-10-19: levelled the bed', '2026-10-20: printed a calibration cube'],
        lines(load_log($path)->entries),
    );
});

test('appending to an existing log keeps what was there', function () {
    $path = fresh_temp_dir() . '/build.log';
    copy(fixture('workshop.log'), $path);
    append_entry($path, new LogEntry('2026-10-19', 'levelled the bed'));
    $log = load_log($path);
    assert_same(4, count($log->entries));
    assert_same('2026-10-19: levelled the bed', format_entry($log->entries[3]));
    assert_same(3, count($log->problems));
});

if ($failures > 0) {
    echo "\n{$failures} failed\n";
    exit(1);
}
