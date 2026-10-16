<?php

declare(strict_types=1);

require_once __DIR__ . '/workshop.php';

const USAGE = <<<'TEXT'
    usage: jig <command> [arguments]

    commands:
      grams <length-mm> <material>   weight of 1.75 mm filament
      check <material> <nozzle-c>    is this nozzle temperature right?
      log <file>                     summarize a Build Log
      help                           show this message

    TEXT;

/** What running jig produced: an exit code and the text for each stream. */
final readonly class Output
{
    public function __construct(
        public int $code,
        public string $stdout = '',
        public string $stderr = '',
    ) {
    }
}

/**
 * Run jig with the given arguments (not including the program name).
 * Never prints and never exits: it returns what should happen.
 *
 * @param list<string> $args
 */
function run(array $args): Output
{
    $rest = array_slice($args, 1);

    return match ($args[0] ?? null) {
        null => new Output(2, stderr: USAGE),
        'help' => new Output(0, stdout: USAGE),
        'grams' => grams_command($rest),
        'check' => check_command($rest),
        'log' => log_command($rest),
        default => error("unknown command: {$args[0]}\nrun 'jig help' to see the commands"),
    };
}

function error(string $message): Output
{
    return new Output(2, stderr: "jig: {$message}\n");
}

/** @param list<string> $args */
function grams_command(array $args): Output
{
    if (count($args) !== 2) {
        return error('usage: jig grams <length-mm> <material>');
    }
    [$lengthText, $materialText] = $args;

    $length = parse_length_mm($lengthText);
    if ($length === null) {
        return error("not a length: {$lengthText}");
    }
    $material = parse_material($materialText);
    if ($material === null) {
        return error("unknown material: {$materialText}");
    }

    return new Output(0, stdout: sprintf("%.2f g\n", filament_grams($length, $material)));
}

/** @param list<string> $args */
function check_command(array $args): Output
{
    if (count($args) !== 2) {
        return error('usage: jig check <material> <nozzle-c>');
    }
    [$materialText, $nozzleText] = $args;

    $material = parse_material($materialText);
    if ($material === null) {
        return error("unknown material: {$materialText}");
    }
    $nozzleC = parse_celsius($nozzleText);
    if ($nozzleC === null) {
        return error("not a temperature: {$nozzleText}");
    }

    $verdict = nozzle_verdict($material, $nozzleC);
    $label = match ($verdict) {
        Verdict::TooCold => 'too cold',
        Verdict::Ok => 'ok',
        Verdict::TooHot => 'too hot',
    };
    [$min, $max] = $material->nozzleRange();

    return new Output(
        $verdict === Verdict::Ok ? 0 : 1,
        stdout: "{$label}: {$material->value} prints at {$min}–{$max} °C\n",
    );
}

/** @param list<string> $args */
function log_command(array $args): Output
{
    if (count($args) !== 1) {
        return error('usage: jig log <file>');
    }
    [$path] = $args;

    try {
        $log = load_log($path);
    } catch (LogFileNotFound) {
        return error("no such file: {$path}");
    }

    $stdout = 'entries: ' . count($log->entries) . "\n"
        . 'problems: ' . count($log->problems) . "\n";
    foreach ($log->problems as $problem) {
        $reason = match (true) {
            $problem->error instanceof MissingSeparator => 'missing separator',
            $problem->error instanceof BadDate => 'bad date',
            default => 'empty text',
        };
        $stdout .= "  line {$problem->lineNumber}: {$reason}\n";
    }

    return new Output($log->problems === [] ? 0 : 1, stdout: $stdout);
}
