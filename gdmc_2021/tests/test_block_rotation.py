import unittest

from utils.blockUtils import BlockRotation, Direction
from utils.structure_serialization import rotate_block_state


def state(block: str) -> dict:
    """Block state properties as a dict, since their order doesn't matter to Minecraft."""
    return dict(prop.split('=') for prop in block.split('[', 1)[1].rstrip(']').split(','))


class TestRotateBlockState(unittest.TestCase):

    def test_east_is_unchanged(self):
        block = "oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]"
        self.assertEqual(block, rotate_block_state(block, Direction.EAST))

    def test_block_without_state_is_unchanged(self):
        for build_direction in Direction:
            self.assertEqual("stone", rotate_block_state("stone", build_direction))

    def test_empty_state_is_unchanged(self):
        # How the structure files store blocks with no state
        for build_direction in Direction:
            self.assertEqual("air[]", rotate_block_state("air[]", build_direction))

    def test_facing(self):
        block = "oak_stairs[facing=east,half=top,shape=straight,waterlogged=false]"
        for build_direction, expected in [(Direction.SOUTH, "south"), (Direction.WEST, "west"), (Direction.NORTH, "north")]:
            with self.subTest(build_direction=build_direction):
                rotated = rotate_block_state(block, build_direction)
                self.assertEqual("oak_stairs[facing={},half=top,shape=straight,waterlogged=false]".format(expected), rotated)

    def test_vertical_facing_is_unchanged(self):
        block = "observer[facing=up,powered=false]"
        self.assertEqual(block, rotate_block_state(block, Direction.SOUTH))

    def test_connections(self):
        block = "oak_fence[east=true,north=false,south=false,waterlogged=false,west=false]"
        rotated = rotate_block_state(block, Direction.SOUTH)
        self.assertTrue(rotated.startswith("oak_fence["))
        self.assertEqual({"south": "true", "east": "false", "west": "false", "waterlogged": "false", "north": "false"},
                         state(rotated))

    def test_connection_values_other_than_booleans(self):
        block = "redstone_wire[east=side,north=none,power=0,south=up,west=none]"
        self.assertEqual({"north": "side", "west": "none", "power": "0", "east": "up", "south": "none"},
                         state(rotate_block_state(block, Direction.NORTH)))

    def test_axis(self):
        for build_direction, expected in [(Direction.SOUTH, "z"), (Direction.WEST, "x"), (Direction.NORTH, "z")]:
            with self.subTest(build_direction=build_direction):
                self.assertEqual("oak_log[axis={}]".format(expected), rotate_block_state("oak_log[axis=x]", build_direction))
        self.assertEqual("oak_log[axis=y]", rotate_block_state("oak_log[axis=y]", Direction.SOUTH))

    def test_sign_rotation(self):
        block = "oak_sign[rotation={},waterlogged=false]".format(BlockRotation.EAST.value)
        for build_direction, expected in [(Direction.SOUTH, BlockRotation.SOUTH), (Direction.WEST, BlockRotation.WEST),
                                          (Direction.NORTH, BlockRotation.NORTH)]:
            with self.subTest(build_direction=build_direction):
                rotated = rotate_block_state(block, build_direction)
                self.assertEqual(str(expected.value), state(rotated)["rotation"])


if __name__ == '__main__':
    unittest.main()
