import unittest

from http_utils import interfaceUtils
from http_utils.worldLoader import WorldSlice
from utils import biomeUtils


class TestBiomeGroupAssignment(unittest.TestCase):
    """
    This doesn't actually do anything yet, and probably won't.
    """

    def setUp(self):
        buildArea = interfaceUtils.requestBuildArea()
        if buildArea == -1:
            self.fail("No build area specified.")
        x1 = buildArea["xFrom"]
        z1 = buildArea["zFrom"]
        x2 = buildArea["xTo"]
        z2 = buildArea["zTo"]
        self.area = (x1, z1, x2 - x1, z2 - z1)
        self.worldSlice = WorldSlice(self.area)
    
    def testBiomeGroupAssigned(self):
        print(self.worldSlice.getBlockCompoundAt([-55,66,-239]))

    def testGetsBiomeID(self):
        """
        Given block's x, y, z find the biome at that block
        :return: None, it's a unit test
        """
        blockPos = (357, 78, -702)
        print(self.worldSlice.getBiomeAt(blockPos))

    def testPrevalentBiome(self):
        biomeGroup = biomeUtils.calculate_prevalent_biome_group(self.area, self.worldSlice)
        self.assertEqual(biomeUtils.BiomeGroup.DEFAULT, biomeGroup)


