from http_utils import interfaceUtils
from structures.minecraft_structure import MinecraftStructure
from utils.biomeUtils import BiomeGroup


class VillageWell(MinecraftStructure):
    """
    A Village Well structure
    https://mcpc.fandom.com/wiki/Tutorials/Creating_a_Village/Well
    """
    def __init__(self, x1: int, y1: int, z1: int, biome_group: 'BiomeGroup'):
        super().__init__(x1, y1, z1, x1+5, y1 + 4, z1+5, biome_group)
        print("Building well with plot (x,y,z): {},{},{}".format(*self.ground_plot[0]))
        self.materials = {
            "default": "stone",
            "fluid": "gold_block",
            "accent": "cobblestone",
            "fence": "oak_fence"
        }

    def build(self) -> None:
        """
        Build the village well structure
        :return:
        """
        for y in range(self.base_elevation - 11, self.base_elevation + 5):
            relative_height = y - self.base_elevation
            print("Building layer {}".format(relative_height))
            if relative_height == -11:
                # well base
                for x in range(self.ground_plot[0][0] + 1, self.ground_plot[1][0]):
                    rel_x = x - self.ground_plot[0][0]
                    for z in range(self.ground_plot[0][2] + 1, self.ground_plot[1][2]):
                        rel_z = z - self.ground_plot[0][2]
                        self.setBlock(x, y, z, self.materials['accent'])
            elif relative_height < 0:
                for x in range(self.ground_plot[0][0] + 1, self.ground_plot[1][0]):
                    rel_x = x - self.ground_plot[0][0]
                    for z in range(self.ground_plot[0][2] + 1, self.ground_plot[1][2]):
                        rel_z = z - self.ground_plot[0][2]
                        if rel_x == 1 or rel_x == 4 or rel_z == 1 or rel_z == 4:
                            self.setBlock(x, y, z, self.materials['accent'])
                        else:
                            self.setBlock(x, y, z, self.materials['fluid'])
            elif relative_height == 0:
                for x in range(self.ground_plot[0][0], self.ground_plot[1][0] + 1):
                    rel_x = x - self.ground_plot[0][0]
                    for z in range(self.ground_plot[0][2], self.ground_plot[1][2] + 1):
                        rel_z = z - self.ground_plot[0][2]
                        if rel_x == 0 or rel_x == 5 or rel_z == 0 or rel_z == 5:
                            self.setBlock(x, y, z, self.materials['default'])
                        elif rel_x == 2 and rel_z in [2,3] or rel_x == 3 and rel_z in [2,3]:
                            self.setBlock(x, y, z, self.materials['fluid'])
                        else:
                            self.setBlock(x, y, z, self.materials['accent'])

            elif relative_height == 1:
                for x in range(self.ground_plot[0][0] + 1, self.ground_plot[1][0]):
                    for z in range(self.ground_plot[0][2] + 1, self.ground_plot[1][2]):
                        if x == self.ground_plot[0][0] + 1 or x == self.ground_plot[0][0] + 4 or z == \
                                self.ground_plot[0][2] + 1 or z == self.ground_plot[0][2] + 4:
                            self.setBlock(x, y, z, self.materials['accent'])
            elif relative_height < 4:
                """Put fences on the corners"""
                self.setBlock(self.ground_plot[0][0] + 1, y, self.ground_plot[0][2] + 1, self.materials['fence'])
                self.setBlock(self.ground_plot[0][0] + 4, y, self.ground_plot[0][2] + 1, self.materials['fence'])
                self.setBlock(self.ground_plot[0][0] + 1, y, self.ground_plot[0][2] + 4, self.materials['fence'])
                self.setBlock(self.ground_plot[0][0] + 4, y, self.ground_plot[0][2] + 4, self.materials['fence'])

            else:
                for x in range(self.ground_plot[0][0] + 1, self.ground_plot[1][0]):
                    for z in range(self.ground_plot[0][2] + 1, self.ground_plot[1][2]):
                        self.setBlock(x, y, z, self.materials['accent'])
