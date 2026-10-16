<?php

declare(strict_types=1);

// From lesson 07, finished.

final readonly class LogEntry
{
    public function __construct(
        public string $date,
        public string $text,
    ) {
    }
}

abstract class InvalidLogLine extends InvalidArgumentException
{
}

final class MissingSeparator extends InvalidLogLine
{
}

final class BadDate extends InvalidLogLine
{
}

final class EmptyText extends InvalidLogLine
{
}

function parse_entry(string $line): LogEntry
{
    $parts = explode(':', $line, 2);
    if (count($parts) < 2) {
        throw new MissingSeparator("no ':' in '{$line}'");
    }
    [$date, $text] = array_map('trim', $parts);
    if (preg_match('/^\d{4}-(\d{2})-(\d{2})$/', $date, $m) !== 1
        || (int) $m[1] < 1 || (int) $m[1] > 12 || (int) $m[2] < 1 || (int) $m[2] > 31
    ) {
        throw new BadDate("not a YYYY-MM-DD date: '{$date}'");
    }
    if ($text === '') {
        throw new EmptyText("no text after the date in '{$line}'");
    }

    return new LogEntry($date, $text);
}

function format_entry(LogEntry $entry): string
{
    return "{$entry->date}: {$entry->text}";
}

// New in this lesson.

final class LogFileNotFound extends RuntimeException
{
}

/** One bad line in a log file. */
final readonly class Problem
{
    public function __construct(
        public int $lineNumber,
        public InvalidLogLine $error,
    ) {
    }
}

/** Everything read from a log file: the good entries and the bad lines. */
final readonly class LoadedLog
{
    /**
     * @param list<LogEntry> $entries
     * @param list<Problem> $problems
     */
    public function __construct(
        public array $entries,
        public array $problems,
    ) {
    }
}

/**
 * @throws LogFileNotFound
 */
function load_log(string $path): LoadedLog
{
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement load_log');
}

function append_entry(string $path, LogEntry $entry): void
{
    // TODO: write the tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement append_entry');
}
