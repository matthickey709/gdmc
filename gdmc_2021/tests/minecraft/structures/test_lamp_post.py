import unittest

from http_utils.worldLoader import WorldSlice
from structures.utilities.lamp_post import LampPost
from tests.helpers import minecraft_build_area_rect, requires_minecraft
from utils.biomeUtils import BiomeGroup


@requires_minecraft
class TestLampPost(unittest.TestCase):
    def setUp(self) -> None:
        self.area = minecraft_build_area_rect()
        self.worldSlice = WorldSlice(self.area)

    def test_build_lamp_post(self):
        y = self.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][1][1]
        lamp = LampPost(self.area[0] + 1, y, self.area[1] + 1, height=5, biome_group=BiomeGroup.DEFAULT)
        lamp.build()


if __name__ == '__main__':
    unittest.main()
