<?php

declare(strict_types=1);

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class FilamentTest extends TestCase
{
    #[Test]
    public function one_metre_of_pla_weighs_about_3_g(): void
    {
        $this->assertEqualsWithDelta(2.98, filament_grams(1000.0, 1.75, 1.24), 0.01);
    }

    /**
     * @return array<string, array{float, float, float}>
     */
    public static function metres(): array
    {
        return [
            '1.75 mm PLA' => [1.75, 1.24, 2.98],
            '2.85 mm PLA' => [2.85, 1.24, 7.91],
            '1.75 mm PETG' => [1.75, 1.27, 3.05],
        ];
    }

    #[Test]
    #[DataProvider('metres')]
    public function a_metre_of_filament_weighs(float $diameterMm, float $density, float $grams): void
    {
        $this->assertEqualsWithDelta($grams, filament_grams(1000.0, $diameterMm, $density), 0.01);
    }

    #[Test]
    public function zero_length_weighs_nothing(): void
    {
        $this->assertEqualsWithDelta(0.0, filament_grams(0.0, 1.75, 1.24), 0.01);
    }

    #[Test]
    public function a_1_kg_spool_of_pla_holds_about_335_m(): void
    {
        $this->assertEqualsWithDelta(335_280.0, filament_length_mm(1000.0, 1.75, 1.24), 50.0);
    }

    #[Test]
    public function length_and_weight_convert_back_and_forth(): void
    {
        $grams = filament_grams(4200.0, 1.75, 1.24);
        $this->assertEqualsWithDelta(4200.0, filament_length_mm($grams, 1.75, 1.24), 0.01);
    }
}
