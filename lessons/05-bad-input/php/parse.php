<?php

declare(strict_types=1);

enum Material: string
{
    case PLA = 'PLA';
    case PETG = 'PETG';
    case ABS = 'ABS';
    case TPU = 'TPU';
}

// The errors. They're given: your job is to throw them.

/** Base class for every way a weight can be invalid. */
abstract class InvalidAmount extends InvalidArgumentException
{
}

final class EmptyInput extends InvalidAmount
{
}

final class NotANumber extends InvalidAmount
{
}

final class NegativeAmount extends InvalidAmount
{
}

final class UnknownMaterial extends InvalidArgumentException
{
}

final class NotEnoughFilament extends DomainException
{
}

/**
 * Grams from text like "250", "12.5 g" or " 40g ".
 *
 * @throws InvalidAmount
 */
function parse_grams(string $text): float
{
    // TODO: replace this line with your implementation.
    throw new RuntimeException('TODO: implement parse_grams');
}

/**
 * A material from text like "PLA" or " petg ".
 *
 * @throws UnknownMaterial
 */
function parse_material(string $text): Material
{
    // TODO: write the tests in test.php first, then replace this line.
    throw new RuntimeException('TODO: implement parse_material');
}

final class Spool
{
    public function __construct(private float $gramsRemaining)
    {
    }

    public function gramsRemaining(): float
    {
        return $this->gramsRemaining;
    }

    /**
     * Use up filament, or refuse and leave the spool unchanged.
     *
     * @throws NotEnoughFilament
     */
    public function consume(float $grams): void
    {
        // TODO: replace this line with your implementation.
        throw new RuntimeException('TODO: implement Spool::consume');
    }
}
