import unittest
import numpy as np

from utils.noiseGenerator import NoiseGenerator
from http_utils.mapUtils import visualize


class TestNoiseGenerators(unittest.TestCase):
    def setUp(self) -> None:
        self.ROWS = 256
        self.COLS = 256

    def test_generate_2d_perlin_noise(self) -> None:
        """
        Test generating perlin noise with varying periods
        :return: None
        """
        periods = 1
        while periods <= 128:
            perlin_noise = NoiseGenerator.generate2DPerlinNoise(self.ROWS, self.COLS, periods)
            visualize(perlin_noise, title="Perlin Noise Periods={}".format(periods))
            periods <<= 1

    def test_generate_2d_fractal_noise(self) -> None:
        """
        Test generating fractal noise with varying octaves
        :return: None
        """
        octaves = 1
        while octaves <= 6:
            fractal_noise = NoiseGenerator.generate2DFractalNoise(self.ROWS, self.COLS, periods=8, octaves=octaves)
            visualize(fractal_noise, title="Fractal Noise Octaves={}".format(octaves))
            octaves += 1


if __name__ == '__main__':
    unittest.main()
