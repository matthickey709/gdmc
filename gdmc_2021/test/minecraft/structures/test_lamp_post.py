import unittest

from http_utils import interfaceUtils
from http_utils.worldLoader import WorldSlice
from structures.utilities.lamp_post import LampPost
from utils.biomeUtils import BiomeGroup


class TestLampPost(unittest.TestCase):
    def setUp(self) -> None:
        buildArea = interfaceUtils.requestBuildArea()
        if buildArea == -1:
            self.fail("No build area specified.")
        x1 = buildArea["xFrom"]
        z1 = buildArea["zFrom"]
        x2 = buildArea["xTo"]
        z2 = buildArea["zTo"]
        self.area = (x1, z1, x2 - x1, z2 - z1)
        self.worldSlice = WorldSlice(self.area)

    def test_build_lamp_post(self):
        y = 69
        lamp = LampPost(590, y, -705, height=5, biome_group=BiomeGroup.DEFAULT)
        lamp.build()


if __name__ == '__main__':
    unittest.main()
