import unittest

import numpy as np

from tests.helpers import set_build_area
from utils.blockUtils import EIGHT_DIRECTIONAL, Movements, heightAt


class TestHeightAt(unittest.TestCase):

    def setUp(self) -> None:
        set_build_area(100, 200, 5, 5)
        self.heightmap = np.arange(25).reshape(5, 5)

    def test_uses_world_coordinates(self):
        self.assertEqual(self.heightmap[2, 3], heightAt(102, 203, self.heightmap))

    def test_outside_heightmap_uses_nearest_edge(self):
        self.assertEqual(self.heightmap[0, 0], heightAt(99, 200, self.heightmap))
        self.assertEqual(self.heightmap[0, 2], heightAt(90, 202, self.heightmap))
        self.assertEqual(self.heightmap[4, 4], heightAt(105, 204, self.heightmap))
        self.assertEqual(self.heightmap[4, 0], heightAt(110, 190, self.heightmap))


class TestMovementBitmask(unittest.TestCase):

    def test_each_direction_round_trips(self):
        for direction in EIGHT_DIRECTIONAL:
            bitmask = Movements.bitmaskFromDirections([direction])
            self.assertEqual([direction], Movements.directionsFromBitmask(bitmask))

    def test_all_directions(self):
        bitmask = Movements.bitmaskFromDirections(EIGHT_DIRECTIONAL)
        self.assertEqual(255, bitmask)
        self.assertCountEqual(EIGHT_DIRECTIONAL, Movements.directionsFromBitmask(bitmask))


if __name__ == '__main__':
    unittest.main()
