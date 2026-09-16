import unittest
from unittest import mock

import numpy as np

from config import Config
from tests.helpers import FakeWorldSlice, set_build_area
from utils.pathfinding import pathfinding_utils
from utils.pathfinding.path_builder import PathBuilder, PathNotFoundError


def path_cost(coordinates):
    cost = 0
    for (x1, z1), (x2, z2) in zip(coordinates, coordinates[1:]):
        diagonal = x1 != x2 and z1 != z2
        cost += Config().heuristic_base_cost_diag if diagonal else Config().heuristic_base_cost
    return cost


class TestPathBuilder(unittest.TestCase):
    SIZE = 40

    def setUp(self) -> None:
        set_build_area(0, 0, self.SIZE, self.SIZE)
        self.heightmap = np.full((self.SIZE, self.SIZE), 64)
        # The real calcGoodHeightmap reads blocks out of the world slice to ignore trees
        patcher = mock.patch("http_utils.mapUtils.calcGoodHeightmap",
                             side_effect=lambda world_slice: world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"])
        patcher.start()
        self.addCleanup(patcher.stop)

    def make_builder(self, start, goal, plots=()):
        world_slice = FakeWorldSlice(self.heightmap)
        legal_actions = pathfinding_utils.determine_legal_actions(world_slice, list(plots))
        path_config = {"path_width": 0, "plots": list(plots)}
        return PathBuilder(start, goal, world_slice, legal_actions, path_config, build_in_minecraft=False)

    def assert_walkable(self, coordinates):
        for (x1, z1), (x2, z2) in zip(coordinates, coordinates[1:]):
            self.assertEqual(1, max(abs(x1 - x2), abs(z1 - z2)), "{} -> {} isn't a single step".format((x1, z1), (x2, z2)))
            climb = abs(int(self.heightmap[x1, z1]) - int(self.heightmap[x2, z2]))
            self.assertLessEqual(climb, 1, "{} -> {} climbs {} blocks".format((x1, z1), (x2, z2), climb))

    def test_finds_shortest_path_on_flat_ground(self):
        start, goal = (2, 3), (30, 12)
        builder = self.make_builder(start, goal)
        builder.determine_path()

        self.assertEqual(start, builder.path_coordinates[0])
        self.assertEqual(goal, builder.path_coordinates[-1])
        self.assert_walkable(builder.path_coordinates)
        # With diagonal moves allowed, the fewest steps is the larger of dx and dz
        self.assertEqual(28 + 1, len(builder.path_coordinates))
        self.assertEqual(1, builder.path[start])
        self.assertEqual(1, builder.path[goal])

    def test_heuristic_matches_path_cost_on_open_ground(self):
        # The heuristic has to be in the same units as the movement costs, otherwise A* barely uses it
        start, goal = (2, 2), (37, 30)
        builder = self.make_builder(start, goal)
        builder.determine_path()

        self.assertEqual(PathBuilder.heuristic(start, goal), path_cost(builder.path_coordinates))

    def test_explores_few_nodes_on_open_ground(self):
        builder = self.make_builder((2, 2), (37, 30))
        builder.determine_path()

        self.assertLess(int(builder.closed.sum()), 0.25 * self.SIZE ** 2)

    def test_unreachable_goal_raises(self):
        # The goal is inside a building plot, which paths can't enter
        builder = self.make_builder((2, 2), (32, 32), plots=[(30, 30, 5, 5)])
        with self.assertRaises(PathNotFoundError):
            builder.determine_path()

    def test_build_path_returns_false_when_no_path(self):
        builder = self.make_builder((2, 2), (32, 32), plots=[(30, 30, 5, 5)])
        with mock.patch("builtins.print"):
            self.assertFalse(builder.build_path())

    def test_goal_outside_build_area_raises(self):
        builder = self.make_builder((2, 2), (self.SIZE + 5, 2))
        with self.assertRaises(PathNotFoundError):
            builder.determine_path()

    def test_path_goes_around_plots(self):
        # A wall of building plot with a gap for z >= 35
        wall = (15, 0, 5, 35)
        builder = self.make_builder((5, 5), (30, 5), plots=[wall])
        builder.determine_path()

        self.assert_walkable(builder.path_coordinates)
        for x, z in builder.path_coordinates:
            self.assertFalse(pathfinding_utils.intersects(x, z, [wall]), "path enters the plot at {}".format((x, z)))

    def test_path_climbs_at_most_one_block_per_step(self):
        # A 10 block cliff at x = 20, with a staircase up it for z >= 35
        self.heightmap[20:, :] = 74
        for x in range(10, 20):
            self.heightmap[x, 35:] = 64 + x - 9
        builder = self.make_builder((5, 5), (30, 5))
        builder.determine_path()

        self.assert_walkable(builder.path_coordinates)
        self.assertTrue(any(z >= 35 for _, z in builder.path_coordinates), "path didn't use the staircase")


if __name__ == '__main__':
    unittest.main()
