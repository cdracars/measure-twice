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
    $text = trim($text);
    if ($text === '') {
        throw new EmptyInput('no weight given');
    }

    $number = str_ends_with($text, 'g') ? rtrim(substr($text, 0, -1)) : $text;
    if (preg_match('/^-?\d+(\.\d+)?$/', $number) !== 1) {
        throw new NotANumber("not a weight: '{$text}'");
    }

    $grams = (float) $number;
    if ($grams < 0) {
        throw new NegativeAmount("weight can't be negative: '{$text}'");
    }

    return $grams;
}

/**
 * A material from text like "PLA" or " petg ".
 *
 * @throws UnknownMaterial
 */
function parse_material(string $text): Material
{
    return Material::tryFrom(strtoupper(trim($text)))
        ?? throw new UnknownMaterial("unknown material: '{$text}'");
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
        if ($grams > $this->gramsRemaining) {
            throw new NotEnoughFilament(
                "need {$grams} g, only {$this->gramsRemaining} g left",
            );
        }

        $this->gramsRemaining -= $grams;
    }
}
