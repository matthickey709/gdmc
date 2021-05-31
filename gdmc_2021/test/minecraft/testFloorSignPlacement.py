import unittest

from utils.blockUtils import BlockRotation
from http_utils.interfaceUtils import setBlock, getBlock


class TestFloorSignPlacement(unittest.TestCase):
    """
    Test suite to test floor sign placement.
    NOTE: Must have Minecraft running with the HTTP mod installed.
    """

    def test_default_orientation(self):
        """
        Test if it is possible to set a sign without specifying a rotation.
        It should face south by default.
        """
        setBlock(63, 64, 160, "oak_sign")
        result = getBlock(63, 64, 160)
        self.assertEqual(result, "minecraft:oak_sign")

    def test_non_default_orientation(self):
        """
        Test if it is possible to set a sign that is facing the non-default (not SOUTH) direction.

        NOTE: As of writing, the HTTP client doesn't return the rotation of the blocks, can only set them.
        Going into the game I can verify that the sign is facing east when this is called. This may be able
        to be done by using the command endpoint of the api.
        """
        setBlock(63, 64, 160, "oak_sign[rotation={}]".format(BlockRotation.EAST.value))
        result = getBlock(63, 64, 160)
        self.assertEqual(result, "minecraft:oak_sign")


if __name__ == "__main__":
    unittest.main()
