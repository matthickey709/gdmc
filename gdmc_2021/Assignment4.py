#####################################################
#   Assignment 4: Write CS4303 near the xz origin
#   in a Minecraft world.
#   Alex Porter (201632205, abporter) & Matthew Hickey (201548278, mjh060)
#####################################################

from http_utils import mapUtils
from http_utils.interfaceUtils import setBlock
from http_utils.worldLoader import WorldSlice


class Assignment4:
    """
    Crude implementation to spell out "CS4303" in a Minecraft world near the origin.
    """

    def __init__(self):
        self.area = (0, 0, 23, 5)
        self.heightmap = None

    def heightAt(self, x, z):
        return self.heightmap[(x - self.area[0], z - self.area[1])]

    def run(self):
        # The message:
        # xxx xxx x x xxx xxx xxx
        # x   x   x x   x x x   x
        # x   xxx xxx xxx x x xxx
        # x     x   x   x x x   x
        # xxx xxx   x xxx xxx xxx
        write = {
            0: [0, 1, 2, 4, 5, 6, 8, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22],
            1: [0, 4, 8, 10, 14, 16, 18, 22],
            2: [0, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 18, 20, 21, 22],
            3: [0, 6, 10, 14, 16, 18, 22],
            4: [0, 1, 2, 4, 5, 6, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22]
        }

        worldSlice = WorldSlice(self.area)

        self.heightmap = mapUtils.calcGoodHeightmap(worldSlice)

        y = self.heightAt(self.area[0], self.area[1])
        print("starting message at {} {} {}".format(self.area[0], y, self.area[1]))
        for x in range(self.area[2]):
            for z in range(self.area[3]):
                if x in write[z]:
                    setBlock(x + self.area[0], y, z + self.area[1], "diamond_block")


def main():
    assign4 = Assignment4()
    assign4.run()


if __name__ == "__main__":
    main()
