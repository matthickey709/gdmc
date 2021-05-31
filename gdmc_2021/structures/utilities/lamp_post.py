from http_utils import interfaceUtils
from structures.minecraft_structure import MinecraftStructure
from utils.biomeUtils import BiomeGroup


class LampPost(MinecraftStructure):
    def __init__(self, x1: int, y1: int, z1: int, height: int = 4, biome_group: 'BiomeGroup' = BiomeGroup.DEFAULT):
        super().__init__(x1, y1, z1, x1, y1 + height, z1, biome_group)
        self.materials = {
            "supports": "oak_fence",
            "light": "glowstone"
        }

    def build(self):
        x, z = self.ground_plot[0][0], self.ground_plot[0][2]
        for y in range(self.base_elevation, self.base_elevation + self.height):
            self.setBlock(x, y, z, self.materials['supports'])
        self.setBlock(x, y, z, self.materials['light'])
