import unittest

from http_utils.worldLoader import WorldSlice
from structures.utilities.village_well import VillageWell
from tests.helpers import minecraft_build_area_rect, requires_minecraft
from utils.biomeUtils import BiomeGroup


@requires_minecraft
class TestVillageWell(unittest.TestCase):

    def setUp(self) -> None:
        self.area = minecraft_build_area_rect()
        self.worldSlice = WorldSlice(self.area)

    def test_generate_village_well(self):
        y = self.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][1][1]
        well_struct = VillageWell(self.area[0] + 1, y, self.area[1] + 1, BiomeGroup.DEFAULT)
        well_struct.build()


if __name__ == '__main__':
    unittest.main()
