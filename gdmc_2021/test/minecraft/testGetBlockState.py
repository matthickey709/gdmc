import unittest
from http_utils import interfaceUtils


class TestGenerateHeightmapViz(unittest.TestCase):
    """
    Class containing "unit tests" for getting block state
    """
    def test_get_block_state(self):
        block_state = interfaceUtils.getBlockState(34, 5, -205)
        print(block_state)

if __name__ == '__main__':
    unittest.main()
