import unittest

from http_utils import interfaceUtils
from http_utils.worldLoader import WorldSlice
from structures.utilities.village_well import VillageWell
from utils.biomeUtils import BiomeGroup


class MyTestCase(unittest.TestCase):

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

    def test_generate_village_well(self):
        y = 71
        well_struct = VillageWell(self.area[0] + 1, y, self.area[1] + 1, BiomeGroup.DEFAULT)
        well_struct.build()


if __name__ == '__main__':
    unittest.main()
