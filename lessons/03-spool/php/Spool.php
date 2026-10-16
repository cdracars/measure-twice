<?php

declare(strict_types=1);

/**
 * A reel of filament, and how much of it is left.
 */
final class Spool
{
    private float $gramsRemaining;

    public function __construct(
        private readonly string $material,
        private readonly float $diameterMm,
        private readonly float $densityGPerCm3,
        float $gramsRemaining,
    ) {
        $this->gramsRemaining = $gramsRemaining;
    }

    public function material(): string
    {
        return $this->material;
    }

    public function gramsRemaining(): float
    {
        return $this->gramsRemaining;
    }

    public function remainingLengthMm(): float
    {
        $areaMm2 = M_PI * ($this->diameterMm / 2) ** 2;
        $gramsPerMm = $areaMm2 / 1000 * $this->densityGPerCm3;

        return $this->gramsRemaining / $gramsPerMm;
    }

    public function canPrint(float $grams): bool
    {
        return $grams <= $this->gramsRemaining;
    }

    /**
     * Use up filament. Callers must check canPrint() first.
     */
    public function consume(float $grams): void
    {
        $this->gramsRemaining -= $grams;
    }
}
