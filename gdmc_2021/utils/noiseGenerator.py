import numpy as np
import random
from perlin_numpy import generate_perlin_noise_2d, generate_fractal_noise_2d


class NoiseGenerator:
    """
    Perlin noise methods from the perlin-numpy package
    """

    @staticmethod
    def generate2DPerlinNoise(height: int, width: int, periods: int = 8, seed: int = 0):
        """
        Generate 2D Perlin Noise grid.
        :param height: Rows in grid.
        :param width: Cols in grid.
        :param periods: Periods of noise to generate along both axes.
        :param seed:
        :return: height x width grid of perlin noise.
        """
        np.random.seed(seed)
        perlin_noise = generate_perlin_noise_2d((height, width), (periods, periods))
        return perlin_noise

    @staticmethod
    def generate2DFractalNoise(height: int, width: int, periods: int = 8, seed: int = 0, octaves: int = 5):
        """
        Combines [octaves] octaves of perlin noise to make fractal noise
        :param height: 2D grid height
        :param width: 2d grid width
        :param periods: periods of noise on both axes
        :param seed: randomizer seed
        :param octaves: number of octaves in the noise
        :return: height x width fractal noise grid
        """
        np.random.seed(seed)
        fractal_noise = generate_fractal_noise_2d((height, width), (periods, periods), octaves)
        return fractal_noise


class ManualFractalNoise:
    """
    Methods for generating fractal noise. From http://devmag.org.za/2009/04/25/perlin-noise/
    """

    @staticmethod
    def interpolate(x0: float, x1: float, alpha: float) -> float:
        return x0 * (1 - alpha) + x1 * alpha

    @staticmethod
    def generateWhiteNoise(width: int, height: int) -> np.array:
        """
        Generate a width x height array with pseudorandom values on [0.0, 1.0)
        :param width: Width of the 2D array
        :param height: Height of the 2D array
        :return: width x height numpy array with random values between 0 and 1
        """
        # Set seed to 0 for testing
        random.seed(0)
        noise = np.zeros((height, width))

        for x in range(width):
            for y in range(height):
                # Random number on [0.0, 1.0)
                noise[y][x] = random.random()

        return noise

    @staticmethod
    def generateSmoothNoise(base_noise: np.array, octave: int) -> np.array:
        """
        TODO: docstring
        :param base_noise:
        :param octave:
        :return: A 2D numpy array representing smooth noise generated
        """
        height, width = base_noise.shape
        smooth_noise = np.full_like(base_noise, 0)
        sample_period = 1 << octave
        sample_frequency = 1.0 / sample_period

        for i in range(width):
            # Calculate the horizontal sampling indices
            sample_i0 = (i // sample_period) * sample_period
            sample_i1 = (sample_i0 + sample_period) % width
            horizontal_blend = (i - sample_i0) * sample_frequency

            for j in range(height):
                # Calculate the vertical sampling indices
                sample_j0 = (j // sample_period) * sample_period
                sample_j1 = (sample_j0 + sample_period) % height
                vertical_blend = (j - sample_j0) * sample_frequency

                # Blend the two top corners
                top = ManualFractalNoise.interpolate(
                    base_noise[sample_j0][sample_i0],
                    base_noise[sample_j0][sample_i1],
                    horizontal_blend)

                # Blend the two bottom corners
                bottom = ManualFractalNoise.interpolate(
                    base_noise[sample_j0][sample_i0],
                    base_noise[sample_j1][sample_i1],
                    horizontal_blend)

                # Final Blend
                smooth_noise[j][i] = ManualFractalNoise.interpolate(top, bottom, vertical_blend)

        return smooth_noise

    @staticmethod
    def generatePerlinNoise(base_noise: np.array, octave_count: int) -> np.array:
        """
        TODO: docstring
        :param base_noise:
        :param octave_count:
        :return:
        """
        height, width = base_noise.shape
        num_octaves = octave_count

        smooth_noise = []

        persistence = 0.5

        # Generate smooth noise
        for i in range(octave_count):
            smooth_noise.append(ManualFractalNoise.generateSmoothNoise(base_noise, i))

        perlin_noise = np.full_like(base_noise, 0)
        amplitude = 1.0
        total_amplitude = 0.0

        # Blend noise together
        for octave in range(octave_count-1, -1, -1):
            amplitude *= persistence
            total_amplitude += amplitude

            for col in range(width):
                for row in range(height):
                    perlin_noise[row][col] += amplitude * smooth_noise[octave][row][col]

        # Normalization
        for col in range(width):
            for row in range(height):
                perlin_noise[row][col] /= total_amplitude

        return perlin_noise
