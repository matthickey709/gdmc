import unittest

from http_utils.worldLoader import WorldSlice
from tests.helpers import minecraft_build_area_rect, requires_minecraft, set_build_area
from utils.pathfinding.path_builder import PathBuilder
from utils.pathfinding.pathfinding_utils import determine_legal_actions, create_graph_from_coordinates, create_mst_from_graph


@requires_minecraft
class TestPathGeneration(unittest.TestCase):

    def setUp(self):
        x, z, x_length, z_length = minecraft_build_area_rect()
        set_build_area(x, z, x_length, z_length)
        self.worldSlice = WorldSlice((x, z, x_length, z_length))
        self.plots = [(x + x_length // 2, z + z_length // 2, 10, 10)]
        self.coordinates = [(x + 5, z + 5), (x + x_length - 6, z + 5), (x + 5, z + z_length - 6)]
        self.path_config = {
            'path_width': 2,
            'paving_block': 'red_concrete',
            'bridge_block': 'oak_planks',
            'plots': self.plots,
            'vertical_clearance': 5,
            'lighting_spawn_rate': 0.01,
            'golem_spawn_rate': 0,
        }
        self.legal_actions = determine_legal_actions(self.worldSlice, self.plots)

    def test_pointA_pointB_pathfinding(self):
        builder = PathBuilder(self.coordinates[0], self.coordinates[1], self.worldSlice, self.legal_actions, self.path_config, True)
        builder.build_path()

    def test_generation_from_mst(self):
        graph = dict(create_graph_from_coordinates(self.coordinates))
        mst = dict(create_mst_from_graph(graph))
        for node in mst.keys():
            for neighbour in list(mst[node]):
                builder = PathBuilder(self.coordinates[node], self.coordinates[neighbour], self.worldSlice, self.legal_actions, self.path_config, True)
                builder.build_path()


if __name__ == '__main__':
    unittest.main()
