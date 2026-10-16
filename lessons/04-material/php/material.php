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
        return match ($this) {
            Material::PLA => 1.24,
            Material::PETG => 1.27,
            Material::ABS => 1.04,
            Material::TPU => 1.21,
        };
    }

    /**
     * Nozzle temperature range in °C, as [min, max].
     *
     * @return array{int, int}
     */
    public function nozzleRange(): array
    {
        return match ($this) {
            Material::PLA => [190, 220],
            Material::PETG => [220, 250],
            Material::ABS => [230, 260],
            Material::TPU => [210, 230],
        };
    }

    public function needsEnclosure(): bool
    {
        return $this === Material::ABS;
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
    [$min, $max] = $material->nozzleRange();

    return match (true) {
        $nozzleC < $min => Verdict::TooCold,
        $nozzleC > $max => Verdict::TooHot,
        default => Verdict::Ok,
    };
}
