import unittest

from config import Config
from http_utils import interfaceUtils
from http_utils.worldLoader import WorldSlice
from utils.pathfinding.pathfinding_utils import determine_legal_actions, intersects


class TestLegalActionGenerator(unittest.TestCase):

    def setUp(self):
        pass
        # buildArea = interfaceUtils.requestBuildArea()
        # if buildArea == -1:
        #     self.fail("No build area specified.")
        # x1 = buildArea["xFrom"]
        # z1 = buildArea["zFrom"]
        # x2 = buildArea["xTo"]
        # z2 = buildArea["zTo"]
        # config = Config()
        # Config().set_build_area_origin(x1, z1)
        # Config().set_build_area_rect(x1, z1, x2, z2)
        # self.area = (x1, z1, x2 - x1, z2 - z1)
        # self.worldSlice = WorldSlice(self.area)

    def test_legal_action_generate(self):
        legal_actions = determine_legal_actions(self.worldSlice, [])
        print(legal_actions)

    def test_intersects(self):
        # This rect represents a 10x10 rectangle with corner at (x,z) == (20, 30)
        rects = [(20, 30, 10, 10)]
        intersect_points = [(20, 30), (29, 39), (20, 39), (29, 30), (25, 35)]
        no_intersect_points = [(19, 29), (30, 40), (25, 25), (15, 35)]
        for point in intersect_points:
            isIntersect = intersects(point[0], point[1], rects)
            self.assertTrue(isIntersect)
        for point in no_intersect_points:
            isIntersect = intersects(point[0], point[1], rects)
            self.assertFalse(isIntersect)


if __name__ == '__main__':
    unittest.main()
