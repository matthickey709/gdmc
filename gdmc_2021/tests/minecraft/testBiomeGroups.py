import unittest

from http_utils.worldLoader import WorldSlice
from tests.helpers import minecraft_build_area_rect, requires_minecraft
from utils import biomeUtils
from utils.blockUtils import Direction


@requires_minecraft
class TestBiomeGroupAssignment(unittest.TestCase):

    def setUp(self):
        self.area = minecraft_build_area_rect()
        self.worldSlice = WorldSlice(self.area)

    def testGetsBiomeID(self):
        """
        Given block's x, y, z find the biome at that block
        :return: None, it's a unit test
        """
        blockPos = (self.area[0], 78, self.area[1])
        self.assertIsNotNone(self.worldSlice.getBiomeAt(blockPos))

    def testPrevalentBiome(self):
        biomeGroup = biomeUtils.calculate_prevalent_biome_group(self.area, self.worldSlice, Direction.EAST)
        self.assertIsInstance(biomeGroup, biomeUtils.BiomeGroup)


if __name__ == '__main__':
    unittest.main()
