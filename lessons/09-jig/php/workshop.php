<?php

declare(strict_types=1);

// Finished pieces from lessons 01–08. You don't need to change this file.

enum Material: string
{
    case PLA = 'PLA';
    case PETG = 'PETG';
    case ABS = 'ABS';
    case TPU = 'TPU';

    public function density(): float
    {
        return match ($this) {
            Material::PLA => 1.24,
            Material::PETG => 1.27,
            Material::ABS => 1.04,
            Material::TPU => 1.21,
        };
    }

    /** @return array{int, int} */
    public function nozzleRange(): array
    {
        return match ($this) {
            Material::PLA => [190, 220],
            Material::PETG => [220, 250],
            Material::ABS => [230, 260],
            Material::TPU => [210, 230],
        };
    }
}

enum Verdict
{
    case TooCold;
    case Ok;
    case TooHot;
}

/** The material, or null if the text isn't one. Ignores case and spaces. */
function parse_material(string $text): ?Material
{
    return Material::tryFrom(strtoupper(trim($text)));
}

/** A length in mm such as "1000" or "12.5", or null if the text isn't one. */
function parse_length_mm(string $text): ?float
{
    $text = trim($text);

    return preg_match('/^\d+(\.\d+)?$/', $text) === 1 ? (float) $text : null;
}

/** A whole number of °C such as "205", or null if the text isn't one. */
function parse_celsius(string $text): ?int
{
    $text = trim($text);

    return preg_match('/^-?\d+$/', $text) === 1 ? (int) $text : null;
}

/** Weight in grams of a length of 1.75 mm filament. */
function filament_grams(float $lengthMm, Material $material): float
{
    $areaMm2 = M_PI * (1.75 / 2) ** 2;

    return $lengthMm * $areaMm2 / 1000 * $material->density();
}

function nozzle_verdict(Material $material, int $nozzleC): Verdict
{
    [$min, $max] = $material->nozzleRange();

    return match (true) {
        $nozzleC < $min => Verdict::TooCold,
        $nozzleC > $max => Verdict::TooHot,
        default => Verdict::Ok,
    };
}

// The Build Log, from lessons 07 and 08.

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

final class LogFileNotFound extends RuntimeException
{
}

final readonly class Problem
{
    public function __construct(
        public int $lineNumber,
        public InvalidLogLine $error,
    ) {
    }
}

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

/**
 * @throws LogFileNotFound
 */
function load_log(string $path): LoadedLog
{
    if (!is_file($path)) {
        throw new LogFileNotFound("no log file at {$path}");
    }
    $contents = file_get_contents($path);
    if ($contents === false) {
        throw new RuntimeException("could not read {$path}");
    }

    $entries = [];
    $problems = [];
    foreach (explode("\n", $contents) as $index => $line) {
        $trimmed = trim($line);
        if ($trimmed === '' || str_starts_with($trimmed, '#')) {
            continue;
        }
        try {
            $entries[] = parse_entry($line);
        } catch (InvalidLogLine $error) {
            $problems[] = new Problem($index + 1, $error);
        }
    }

    return new LoadedLog($entries, $problems);
}
