import unittest
import numpy as np

from utils.noiseGenerator import ManualFractalNoise, NoiseGenerator


class TestNoiseGenerators(unittest.TestCase):
    # perlin-numpy needs the shape to be a multiple of periods * 2^(octaves - 1)
    ROWS = 64
    COLS = 128

    def test_generate_2d_perlin_noise(self) -> None:
        """
        Test generating perlin noise with varying periods
        :return: None
        """
        periods = 1
        while periods <= 64:
            with self.subTest(periods=periods):
                perlin_noise = NoiseGenerator.generate2DPerlinNoise(self.ROWS, self.COLS, periods)
                self.assertEqual((self.ROWS, self.COLS), perlin_noise.shape)
                self.assertTrue(np.all(np.abs(perlin_noise) <= 1))
            periods <<= 1

    def test_generate_2d_fractal_noise(self) -> None:
        """
        Test generating fractal noise with varying octaves
        :return: None
        """
        for octaves in range(1, 5):
            with self.subTest(octaves=octaves):
                fractal_noise = NoiseGenerator.generate2DFractalNoise(self.ROWS, self.COLS, periods=8, octaves=octaves)
                self.assertEqual((self.ROWS, self.COLS), fractal_noise.shape)
                self.assertTrue(np.all(np.abs(fractal_noise) <= 2))

    def test_same_seed_gives_same_noise(self) -> None:
        first = NoiseGenerator.generate2DPerlinNoise(self.ROWS, self.COLS, seed=7)
        second = NoiseGenerator.generate2DPerlinNoise(self.ROWS, self.COLS, seed=7)
        np.testing.assert_array_equal(first, second)


class TestManualFractalNoise(unittest.TestCase):

    def test_smooth_noise_at_octave_zero_is_unchanged(self) -> None:
        base_noise = ManualFractalNoise.generateWhiteNoise(8, 4)
        np.testing.assert_array_equal(base_noise, ManualFractalNoise.generateSmoothNoise(base_noise, 0))

    def test_smooth_noise_blends_between_rows(self) -> None:
        # Each value is its row number, so halfway between the samples at rows 0 and 2 should be 1
        base_noise = np.repeat(np.arange(4.0)[:, None], 4, axis=1)
        smooth_noise = ManualFractalNoise.generateSmoothNoise(base_noise, 1)
        self.assertAlmostEqual(1.0, smooth_noise[1][0])


if __name__ == '__main__':
    unittest.main()
