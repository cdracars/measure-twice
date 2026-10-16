<?php

declare(strict_types=1);

/**
 * Grams per millimetre of filament.
 */
function grams_per_mm(float $diameterMm, float $densityGPerCm3): float
{
    $radiusMm = $diameterMm / 2;
    $areaMm2 = M_PI * $radiusMm ** 2;
    $cm3PerMm = $areaMm2 / 1000;

    return $cm3PerMm * $densityGPerCm3;
}

/**
 * Weight in grams of a length of filament.
 */
function filament_grams(float $lengthMm, float $diameterMm, float $densityGPerCm3): float
{
    return $lengthMm * grams_per_mm($diameterMm, $densityGPerCm3);
}

/**
 * Length in millimetres of a weight of filament.
 */
function filament_length_mm(float $grams, float $diameterMm, float $densityGPerCm3): float
{
    return $grams / grams_per_mm($diameterMm, $densityGPerCm3);
}
