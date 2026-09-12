import unittest

from utils.pathfinding.pathfinding_utils import graph_node_for_building_plot
from utils.blockUtils import Direction


class TestNodeFromPlot(unittest.TestCase):

    def setUp(self) -> None:
        self.plot = (-40, -50, 100, 30)

    def test_entrance_north(self):
        node = graph_node_for_building_plot(self.plot, Direction.NORTH)
        expected = (10, -51)
        self.assertEqual(expected, node)

    def test_entrance_east(self):
        node = graph_node_for_building_plot(self.plot, Direction.EAST)
        expected = (61, -35)
        self.assertEqual(expected, node)

    def test_entrance_south(self):
        node = graph_node_for_building_plot(self.plot, Direction.SOUTH)
        expected = (10, -19)
        self.assertEqual(expected, node)

    def test_entrance_west(self):
        node = graph_node_for_building_plot(self.plot, Direction.WEST)
        expected = (-41, -35)
        self.assertEqual(expected, node)


if __name__ == '__main__':
    unittest.main()
