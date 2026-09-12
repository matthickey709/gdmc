import unittest

import numpy as np

from tests.helpers import FakeWorldSlice, set_build_area
from utils.blockUtils import EIGHT_DIRECTIONAL, Movements
from utils.pathfinding.pathfinding_utils import determine_legal_actions, intersects


class TestIntersects(unittest.TestCase):

    def test_intersects(self):
        # This rect represents a 10x10 rectangle with corner at (x,z) == (20, 30)
        rects = [(20, 30, 10, 10)]
        intersect_points = [(20, 30), (29, 39), (20, 39), (29, 30), (25, 35)]
        no_intersect_points = [(19, 29), (30, 40), (25, 25), (15, 35)]
        for point in intersect_points:
            self.assertTrue(intersects(point[0], point[1], rects), point)
        for point in no_intersect_points:
            self.assertFalse(intersects(point[0], point[1], rects), point)


class TestLegalActions(unittest.TestCase):

    def setUp(self) -> None:
        # Not at the origin, to check world and local coordinates aren't mixed up
        set_build_area(100, 200, 10, 10)
        self.heightmap = np.full((10, 10), 64)

    def actions_at(self, local_x, local_z, plots=()):
        legal_actions = determine_legal_actions(FakeWorldSlice(self.heightmap), list(plots))
        return sorted(tuple(d) for d in Movements.directionsFromBitmask(legal_actions[local_x][local_z]))

    def test_open_ground_allows_all_eight_directions(self):
        self.assertEqual(sorted(tuple(d) for d in EIGHT_DIRECTIONAL), self.actions_at(5, 5))

    def test_cannot_leave_build_area(self):
        self.assertEqual(sorted([(1, 0), (0, 1), (1, 1)]), self.actions_at(0, 0))
        self.assertEqual(sorted([(-1, 0), (0, -1), (-1, -1)]), self.actions_at(9, 9))

    def test_can_climb_one_block(self):
        self.heightmap[6, :] = 65
        self.assertIn((1, 0), self.actions_at(5, 5))

    def test_cannot_climb_two_blocks(self):
        self.heightmap[6, :] = 66
        self.assertNotIn((1, 0), self.actions_at(5, 5))
        self.assertIn((-1, 0), self.actions_at(5, 5))

    def test_cannot_enter_plots(self):
        # World coordinates, starting directly east of local (5, 5)
        plot = (106, 205, 3, 3)
        actions = self.actions_at(5, 5, plots=[plot])
        self.assertNotIn((1, 0), actions)
        self.assertIn((-1, 0), actions)


if __name__ == '__main__':
    unittest.main()
