import unittest
import utils.pathfinding.pathfinding_utils as pathfinding


class TestMSTAlgorithm(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = {
            0: {1: 2, 2: 3},
            1: {0: 2, 2: 1, 3: 1, 4: 4},
            2: {0: 3, 1: 1, 5: 5},
            3: {1: 1, 4: 1},
            4: {1: 4, 3: 1, 5: 1},
            5: {2: 5, 4: 1, 6: 1},
            6: {5: 1},
        }
        self.coordinates = [(3, 0), (0, 1), (3, 2), (1, 3)]

    def test_mst_generation(self):
        result = dict(pathfinding.create_mst_from_graph(self.graph))
        expected = {0: {1}, 1: {2, 3}, 3: {4}, 4: {5}, 5: {6}}
        self.assertEqual(result, expected)

    def test_graph_from_coordinates_generation(self):
        result = dict(pathfinding.create_graph_from_coordinates(self.coordinates))
        expected = {0: {1: 3.1622776601683795, 2: 2.0, 3: 3.605551275463989},
                    1: {0: 3.1622776601683795, 2: 3.1622776601683795, 3: 2.23606797749979},
                    2: {0: 2.0, 1: 3.1622776601683795, 3: 2.23606797749979},
                    3: {0: 3.605551275463989, 1: 2.23606797749979, 2: 2.23606797749979}}
        self.assertEqual(result, expected)

    def test_coordinates_to_mst(self):
        graph = dict(pathfinding.create_graph_from_coordinates(self.coordinates))
        mst = dict(pathfinding.create_mst_from_graph(graph))
        expected = {0: {2}, 2: {3}, 3: {1}}
        self.assertEqual(mst, expected)


if __name__ == '__main__':
    unittest.main()
