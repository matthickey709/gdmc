import unittest

from http_utils.interfaceUtils import setBlock


class TestBlockOptions(unittest.TestCase):

    def test_snowy_grass(self):
        setBlock(960, 66, -49, "snow_block")


if __name__ == '__main__':
    unittest.main()
