from utils.biomeUtils import BiomeGroup
from utils import blockUtils


class MinecraftStructure:
    """
    Base class for all generated structures for the Minecraft world.
    """
    def __init__(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, biome_group: 'BiomeGroup'):
        self.ground_plot = ((x1, y1, z1), (x2, y1, z2))
        self.height = y2 - y1
        self.base_elevation = y1
        self.biome_group = biome_group

    def build(self):
        """
        Build the structure. Overridden in subclasses
        :return: None, modify minecraft world
        """
        pass

    def setBlock(self, x, y, z, block) -> None:
        """
        Set a block in the Minecraft world given an x,y,z coordinate and block type
        :param x:
        :param y:
        :param z:
        :param block: namespaced id of the block to place
        :return: None, sets block in minecraft world
        """
        blockUtils.setBlock(x, y, z, block)

