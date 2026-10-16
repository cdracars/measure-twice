<?php

declare(strict_types=1);

/**
 * A reel of filament, and how much of it is left.
 */
final class Spool
{
    // TODO: declare the properties a spool needs. Keep the remaining grams
    // private, so only consume() can change them.

    public function __construct(
        string $material,
        float $diameterMm,
        float $densityGPerCm3,
        float $gramsRemaining,
    ) {
        // TODO: replace this line with your implementation.
        throw new RuntimeException('TODO: implement Spool::__construct');
    }

    public function material(): string
    {
        throw new RuntimeException('TODO: implement Spool::material');
    }

    public function gramsRemaining(): float
    {
        throw new RuntimeException('TODO: implement Spool::gramsRemaining');
    }

    public function remainingLengthMm(): float
    {
        throw new RuntimeException('TODO: implement Spool::remainingLengthMm');
    }

    public function canPrint(float $grams): bool
    {
        throw new RuntimeException('TODO: implement Spool::canPrint');
    }

    /**
     * Use up filament. Callers must check canPrint() first.
     */
    public function consume(float $grams): void
    {
        // TODO: write the tests in test.php first, then replace this line.
        throw new RuntimeException('TODO: implement Spool::consume');
    }
}
