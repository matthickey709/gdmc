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

    def test_block_without_equivalent_is_unchanged(self):
        block = "oak_planks"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.WARM)
        self.assertEqual(block, new_block)

    def test_sand_default(self):
        new_block = biomeUtils.get_biome_equivalent("sand", biomeUtils.BiomeGroup.DEFAULT)
        self.assertEqual("grass_block", new_block)

    def test_state_is_dropped_from_replacement_without_facing(self):
        block = "scaffolding[bottom=false,distance=0,waterlogged=false]"
        new_block = biomeUtils.get_biome_equivalent(block, biomeUtils.BiomeGroup.DEFAULT)
        self.assertEqual("oak_planks", new_block)

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
