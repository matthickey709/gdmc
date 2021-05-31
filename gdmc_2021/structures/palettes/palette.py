from utils.biomeUtils import BiomeGroup

DEFAULT_DEFAULT = "oak_planks"
SNOW_DEFAULT = "spruce_planks"
COLD_DEFAULT = DEFAULT_DEFAULT
TROPICAL_DEFAULT = "jungle_planks"
WARM_DEFAULT = "chiseled_sandstone"
OCEAN_DEFAULT = DEFAULT_DEFAULT
RUGGED_DEFAULT = "chiseled_stone_bricks"
RUNNING_WATER_DEFAULT = DEFAULT_DEFAULT


class Palette:
    """
    Base palette class for structures.
    """
    def __init__(self, biome_group: 'BiomeGroup'):
        """
        Base constructor for generating a palette for a structure given a biome group
        :param biome_group: Biome group that the structure will be built in.
        """
        self.biome_group = biome_group
        self.materials = self.setDefaultMaterials()

    def setDefaultMaterials(self) -> dict:
        """
        Set the base materials for the biome group
        :return: Dictionary with key = material purpose, value = material (namespaced id)
        """
        mats = {}
        if self.biome_group == BiomeGroup.SNOW:
            mats['default'] = SNOW_DEFAULT
        elif self.biome_group == BiomeGroup.COLD:
            mats['default'] = COLD_DEFAULT
        elif self.biome_group == BiomeGroup.WARM:
            mats['default'] = WARM_DEFAULT
        elif self.biome_group == BiomeGroup.TROPICAL:
            mats['default'] = TROPICAL_DEFAULT
        elif self.biome_group == BiomeGroup.RUGGED:
            mats['default'] = RUGGED_DEFAULT
        elif self.biome_group == BiomeGroup.OCEAN:
            mats['default'] = OCEAN_DEFAULT
        elif mats['default'] == BiomeGroup.RUNNING_WATER:
            mats['default'] = RUNNING_WATER_DEFAULT
        else:
            mats['default'] = DEFAULT_DEFAULT
        return mats
