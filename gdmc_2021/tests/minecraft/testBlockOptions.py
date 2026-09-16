import unittest

from http_utils.interfaceUtils import getBlock, setBlock
from tests.helpers import MINECRAFT_BUILD_AREA, requires_minecraft


@requires_minecraft
class TestBlockOptions(unittest.TestCase):

    def test_snowy_grass(self):
        x, y, z = MINECRAFT_BUILD_AREA["xFrom"], MINECRAFT_BUILD_AREA["yFrom"], MINECRAFT_BUILD_AREA["zFrom"]
        setBlock(x, y, z, "snow_block")
        self.assertEqual("minecraft:snow_block", getBlock(x, y, z))


if __name__ == '__main__':
    unittest.main()
