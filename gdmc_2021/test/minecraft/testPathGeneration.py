import unittest

from config import Config
from http_utils import interfaceUtils
from http_utils.worldLoader import WorldSlice
from utils.pathfinding.path_builder import PathBuilder
from utils.pathfinding.pathfinding_utils import determine_legal_actions, create_graph_from_coordinates, create_mst_from_graph


class TestPathGeneration(unittest.TestCase):

    def setUp(self):
        buildArea = interfaceUtils.requestBuildArea()
        if buildArea == -1:
            self.fail("No build area specified.")
        x1 = buildArea["xFrom"]
        z1 = buildArea["zFrom"]
        x2 = buildArea["xTo"]
        z2 = buildArea["zTo"]
        self.config = Config()
        Config().set_build_area_origin(x1, z1)
        Config().set_build_area_rect(x1, z1, x2, z2)
        self.area = (x1, z1, x2 - x1, z2 - z1)
        self.worldSlice = WorldSlice(self.area)
        self.plots = [(745, -75, 10, 10)]
        self.coordinates = [(683, -77), (643, -134), (633, -103)]
        self.path_config = {
            'path_width': 2,
            'paving_block': 'red_concrete',
            'bridge_block': 'oak_planks',
            'plots': self.plots,
            'vertical_clearance': 5,
            'lighting_spawn_rate': 0.01,
        }
        self.legal_actions = determine_legal_actions(self.worldSlice, self.plots)

    def test_pointA_pointB_pathfinding(self):
        builder = PathBuilder((1114, 1495), (1184, 1482), self.worldSlice, self.legal_actions, self.path_config, True)
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
