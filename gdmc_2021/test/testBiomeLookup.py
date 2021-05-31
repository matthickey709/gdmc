import unittest

from utils import biomeUtils


class TestBiomeLookup(unittest.TestCase):

    def test_grass_block_snow(self):
        block = "grass_block"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.SNOW)
        self.assertEqual("snow_block", new_block)

    def test_grass_block_default(self):
        block = "grass_block"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.DEFAULT)
        self.assertEqual(block, new_block)

    def test_plank_desert(self):
        blocks = ["oak_planks", "cedar_planks", "birch_planks"]
        for block in blocks:
            new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.WARM)
            self.assertEqual("cut_sandstone", new_block)

    def test_cobble_default(self):
        block = "cobblestone"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.DEFAULT)
        self.assertEqual(block, new_block)

    def test_stone_default(self):
        block = "stone"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.DEFAULT)
        self.assertEqual(block, new_block)


if __name__ == '__main__':
    unittest.main()
