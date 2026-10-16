<?php

declare(strict_types=1);

use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class FilamentTest extends TestCase
{
    #[Test]
    public function one_metre_of_pla_weighs_about_3_g(): void
    {
        $this->assertEqualsWithDelta(2.98, filament_grams(1000.0, 1.75, 1.24), 0.01);
    }

    // TODO: port the rest of lesson 01's tests (lessons/01-filament-math/php/test.php).
    // Use a data provider (#[DataProvider]) for the "grams of a metre" cases.
}
