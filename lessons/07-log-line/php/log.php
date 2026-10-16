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
    $parts = explode(':', $line, 2);
    if (count($parts) < 2) {
        throw new MissingSeparator("no ':' in '{$line}'");
    }

    [$date, $text] = array_map('trim', $parts);
    if (!is_valid_date($date)) {
        throw new BadDate("not a YYYY-MM-DD date: '{$date}'");
    }
    if ($text === '') {
        throw new EmptyText("no text after the date in '{$line}'");
    }

    return new LogEntry($date, $text);
}

/**
 * Whether a string looks like YYYY-MM-DD. Checks the shape, not the calendar.
 */
function is_valid_date(string $date): bool
{
    if (preg_match('/^(\d{4})-(\d{2})-(\d{2})$/', $date, $matches) !== 1) {
        return false;
    }
    $month = (int) $matches[2];
    $day = (int) $matches[3];

    return $month >= 1 && $month <= 12 && $day >= 1 && $day <= 31;
}

/**
 * The line for an entry: "YYYY-MM-DD: text".
 */
function format_entry(LogEntry $entry): string
{
    return "{$entry->date}: {$entry->text}";
}

/**
 * The text if it has at most $maxChars characters, otherwise its first
 * $maxChars characters followed by "…".
 */
function truncate(string $text, int $maxChars): string
{
    if (mb_strlen($text) <= $maxChars) {
        return $text;
    }

    return mb_substr($text, 0, $maxChars) . '…';
}
