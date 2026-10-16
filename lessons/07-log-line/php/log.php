<?php

declare(strict_types=1);

final readonly class LogEntry
{
    public function __construct(
        public string $date,
        public string $text,
    ) {
    }
}

// The errors. They're given: your job is to throw them.

/** Base class for every way a log line can be invalid. */
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

/**
 * A log entry from a line like "2026-10-16: replaced nozzle".
 *
 * @throws InvalidLogLine
 */
function parse_entry(string $line): LogEntry
{
    // TODO: write the error tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement parse_entry');
}

/**
 * The line for an entry: "YYYY-MM-DD: text".
 */
function format_entry(LogEntry $entry): string
{
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement format_entry');
}

/**
 * The text if it has at most $maxChars characters, otherwise its first
 * $maxChars characters followed by "…".
 */
function truncate(string $text, int $maxChars): string
{
    throw new RuntimeException('TODO: implement truncate');
}
