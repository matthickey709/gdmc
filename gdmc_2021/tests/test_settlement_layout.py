import contextlib
import io
import unittest
from unittest import mock

import numpy as np

from GDMCSettlementGenerator import GDMCSettlementGenerator
from tests.helpers import set_build_area
from utils import structure_serialization
from utils.blockUtils import Direction
from utils.structure import Structure


class TestStructurePlacement(unittest.TestCase):

    @staticmethod
    def built_footprint(data, corner, build_direction):
        """
        :return: (min x, max x, min z, max z) of the blocks build_from_3d_array places
        """
        placed = []
        with mock.patch("utils.blockUtils.setBlock", side_effect=lambda x, y, z, block: placed.append((x, z))), \
                mock.patch("http_utils.interfaceUtils.sendBlocks"), \
                contextlib.redirect_stdout(io.StringIO()):
            structure_serialization.build_from_3d_array(data, corner, build_dir=build_direction)
        xs = [x for x, _ in placed]
        zs = [z for _, z in placed]
        return min(xs), max(xs), min(zs), max(zs)

    def test_rotated_structure_covers_its_plot(self):
        # Not square, so mixing up length and width shows up. 15 along x and 11 along z as serialized.
        serialized_length, serialized_width = 15, 11
        data = np.full((serialized_length, serialized_width, 2), "stone", dtype=object)
        x, z = 40, 70
        for build_direction in Direction:
            with self.subTest(build_direction=build_direction):
                length, width = serialized_length, serialized_width
                if build_direction in (Direction.NORTH, Direction.SOUTH):
                    length, width = width, length
                genx, genz = GDMCSettlementGenerator.build_origin_for_plot(x, z, length, width, build_direction)

                plot = (x, x + length - 1, z, z + width - 1)
                self.assertEqual(plot, self.built_footprint(data, (genx, 64, genz), build_direction))


class TestPerimeterFence(unittest.TestCase):
    AREA = (10, 20, 100, 60)

    def sides(self):
        xs, zs, xl, zl = self.AREA
        return {
            "north": [(x, zs) for x in range(xs, xs + xl)],
            "south": [(x, zs + zl - 1) for x in range(xs, xs + xl)],
            "west": [(xs, z) for z in range(zs, zs + zl)],
            "east": [(xs + xl - 1, z) for z in range(zs, zs + zl)],
        }

    def test_perimeter_visits_each_edge_block_once(self):
        coords = list(GDMCSettlementGenerator.perimeter_coordinates(self.AREA))
        expected = set().union(*self.sides().values())

        self.assertEqual(len(expected), len(coords))
        self.assertEqual(expected, set(coords))

    def test_every_side_has_a_gate_in_the_middle(self):
        for side, coords in self.sides().items():
            with self.subTest(side=side):
                gate = [c for c in coords if not GDMCSettlementGenerator.should_build_fence(*c, self.AREA)]
                self.assertEqual(len(coords) // 5, len(gate))
                # The gate is one contiguous opening in the middle of the side
                start = coords.index(gate[0])
                self.assertEqual(coords[start:start + len(gate)], gate)
                self.assertIn(coords[len(coords) // 2], gate)

    def test_corners_are_fenced(self):
        xs, zs, xl, zl = self.AREA
        for corner in [(xs, zs), (xs + xl - 1, zs), (xs, zs + zl - 1), (xs + xl - 1, zs + zl - 1)]:
            self.assertTrue(GDMCSettlementGenerator.should_build_fence(*corner, self.AREA), corner)

    def test_area_inside_fence_is_just_inside_it(self):
        inside = GDMCSettlementGenerator.area_inside_fence(self.AREA)
        fence = set(GDMCSettlementGenerator.perimeter_coordinates(self.AREA))
        inside_edge = set(GDMCSettlementGenerator.perimeter_coordinates(inside))

        self.assertEqual(set(), fence & inside_edge)
        # Every block inside the fence's edge is next to the fence
        for x, z in inside_edge:
            neighbours = {(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)}
            self.assertTrue(neighbours & fence, (x, z))


class TestPlotFlatness(unittest.TestCase):

    def setUp(self) -> None:
        set_build_area(100, 100, 20, 20)
        # Skip __init__, which needs Minecraft running
        self.generator = GDMCSettlementGenerator.__new__(GDMCSettlementGenerator)
        self.generator.HEIGHTMAP = np.full((20, 20), 64)
        # Covers local x 5..8 and z 5..10
        self.plot = Structure(105, 105, 4, 6, Direction.EAST)

    def test_flat_plot(self):
        self.assertEqual((1.0, 64), self.generator.get_plot_flatness(self.plot))

    def test_every_corner_affects_flatness(self):
        for corner in [(5, 5), (5, 10), (8, 5), (8, 10)]:
            with self.subTest(corner=corner):
                self.generator.HEIGHTMAP = np.full((20, 20), 64)
                self.generator.HEIGHTMAP[corner] = 70
                flatness, _ = self.generator.get_plot_flatness(self.plot)
                self.assertGreater(flatness, 1)

    def test_height_is_median_of_whole_plot(self):
        self.generator.HEIGHTMAP[5:9, 5:11] = 70
        # The furthest row of the plot (6 of its 24 blocks) is lower
        self.generator.HEIGHTMAP[8, 5:11] = 60
        _, height = self.generator.get_plot_flatness(self.plot)
        self.assertEqual(70, height)


if __name__ == '__main__':
    unittest.main()
