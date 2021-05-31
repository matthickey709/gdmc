from structures.minecraft_structure import MinecraftStructure


class StandardHouse(MinecraftStructure):
    """
    TODO: Class representing a standard house
    """
    def __init__(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, biome_group: 'BiomeGroup'):
        super().__init__(x1, y1, z1, x2, y2, z2, biome_group)
