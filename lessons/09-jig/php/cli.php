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
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement run');
}
