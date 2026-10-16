<?php

declare(strict_types=1);

/**
 * Whether a nozzle temperature suits a material:
 * "too cold", "ok", "too hot", or "unknown material".
 */
function nozzle_verdict(string $material, int $nozzleC): string
{
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement nozzle_verdict');
}

/**
 * Whether a material needs an enclosed printer.
 */
function needs_enclosure(string $material): bool
{
    // TODO: write the tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement needs_enclosure');
}
