<?php

declare(strict_types=1);

/**
 * Whether a nozzle temperature suits a material:
 * "too cold", "ok", "too hot", or "unknown material".
 */
function nozzle_verdict(string $material, int $nozzleC): string
{
    $range = match ($material) {
        'PLA' => [190, 220],
        'PETG' => [220, 250],
        'ABS' => [230, 260],
        'TPU' => [210, 230],
        default => null,
    };

    if ($range === null) {
        return 'unknown material';
    }

    [$min, $max] = $range;

    return match (true) {
        $nozzleC < $min => 'too cold',
        $nozzleC > $max => 'too hot',
        default => 'ok',
    };
}

/**
 * Whether a material needs an enclosed printer.
 */
function needs_enclosure(string $material): bool
{
    return $material === 'ABS';
}
