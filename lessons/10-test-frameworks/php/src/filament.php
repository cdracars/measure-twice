<?php

declare(strict_types=1);

// Lesson 01's solution. In this lesson the code is finished; the tests move.

function grams_per_mm(float $diameterMm, float $densityGPerCm3): float
{
    $areaMm2 = M_PI * ($diameterMm / 2) ** 2;

    return $areaMm2 / 1000 * $densityGPerCm3;
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
