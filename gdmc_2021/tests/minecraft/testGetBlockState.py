import unittest

from http_utils import interfaceUtils
from tests.helpers import MINECRAFT_BUILD_AREA, requires_minecraft


@requires_minecraft
class TestGetBlockState(unittest.TestCase):
    """
    Class containing "unit tests" for getting block state
    """
    def test_get_block_state(self):
        block_state = interfaceUtils.getBlockState(MINECRAFT_BUILD_AREA["xFrom"], MINECRAFT_BUILD_AREA["yFrom"],
                                                   MINECRAFT_BUILD_AREA["zFrom"])
        self.assertTrue(block_state.startswith("minecraft:"), block_state)


if __name__ == '__main__':
    unittest.main()
