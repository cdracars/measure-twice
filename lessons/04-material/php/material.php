<?php

declare(strict_types=1);

enum Material: string
{
    case PLA = 'PLA';
    case PETG = 'PETG';
    case ABS = 'ABS';
    case TPU = 'TPU';

    /** Density in g/cm³. */
    public function density(): float
    {
        // TODO: replace this line with your implementation.
        throw new RuntimeException('TODO: implement Material::density');
    }

    /**
     * Nozzle temperature range in °C, as [min, max].
     *
     * @return array{int, int}
     */
    public function nozzleRange(): array
    {
        throw new RuntimeException('TODO: implement Material::nozzleRange');
    }

    public function needsEnclosure(): bool
    {
        throw new RuntimeException('TODO: implement Material::needsEnclosure');
    }
}

enum Verdict
{
    case TooCold;
    case Ok;
    case TooHot;
}

function nozzle_verdict(Material $material, int $nozzleC): Verdict
{
    // TODO: write the boundary tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement nozzle_verdict');
}
