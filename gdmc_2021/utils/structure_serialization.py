import numpy as np

from config import Config
from http_utils import interfaceUtils
from utils import blockUtils
from utils.blockUtils import Direction
from utils import biomeUtils

RELATIVE_ROTATIONS = {
    # East is no-op
    Direction.EAST: {
        "east": "east",
        "south": "south",
        "west": "west",
        "north": "north"
    },
    Direction.SOUTH: {
        # Facing directions move 90 CW
        "east": "south",
        "south": "west",
        "west": "north",
        "north": "east"
    },
    Direction.WEST: {
        # 180 Rot
        "east": "west",
        "south": "north",
        "west": "east",
        "north": "south"
    },
    Direction.NORTH: {
        # 90 deg CCW
        "east": "north",
        "south": "east",
        "west": "south",
        "north": "west"
    }
}

# Number of 90 degree clockwise turns from the serialized (EAST) orientation
QUARTER_TURNS_CW = {
    Direction.EAST: 0,
    Direction.SOUTH: 1,
    Direction.WEST: 2,
    Direction.NORTH: 3
}


def getBlock(x, y, z) -> str:
    return interfaceUtils.getBlockState(x, y, z)


def serialize_rect_prism(corner1: (int, int), corner2: (int, int), ground_height: int, max_height: int):
    """

    :param corner1: (x,z) coordinate of lowest x,z corner
    :param corner2: (x,z) coordinate of greatest x,z corner
    :param ground_height: y value of ground height
    :param max_height: y value of highest point on structure
    :return: numpy array indexed as [y][x][z] in local coordinates (corner1 is (0,0,0))
    """
    x_spread = corner2[0] - corner1[0] + 1
    z_spread = corner2[1] - corner1[1] + 1
    y_spread = max_height - ground_height + 1
    data = np.empty((x_spread, z_spread, y_spread), dtype=object)
    print("beginning serialization of {} layers...".format(max_height - ground_height + 1))
    for y in range(ground_height, max_height + 1):
        for x in range(corner1[0], corner2[0] + 1):
            for z in range(corner1[1], corner2[1] + 1):
                block = getBlock(x, y, z)
                block = block.split(':')
                # print("{},{},{}={}".format(x, y, z, block[1]))
                data[x - corner1[0]][z - corner1[1]][y - ground_height] = block[1]
        print("Done layer {} of {}".format(y - ground_height + 1, max_height - ground_height + 1))

    return data


def save_3d_to_file(filename: str, data: np.array) -> None:
    reshaped = data.reshape(data.shape[0], -1)
    np.savetxt(filename, reshaped, fmt='%s')


def reload_3d_from_file(filename: str, shaping_factor: int) -> np.array:
    """

    :param filename:
    :param shaping_factor: how many blocks (inclusive) from the lowest point of the structure to the highest
    :return:
    """
    loaded = np.loadtxt(filename, dtype=str)
    to_return = loaded.reshape(loaded.shape[0], loaded.shape[1] // shaping_factor, shaping_factor)
    return to_return


def rotate_block_state(block: str, build_dir: 'Direction') -> str:
    """
    Rotates the directional parts of a block's state so the block matches a structure built in build_dir.
    Handles facing=<direction>, connections keyed by direction (e.g. fences' north=true, redstone's east=side),
    axis=x|z (e.g. logs) and the 16-step rotation=<n> used by signs and banners.
    :param block: block id with optional state, e.g. oak_stairs[facing=east,half=bottom]
    :param build_dir: the direction the structure is being built in. EAST is how structures were serialized.
    :return: the block with its state rotated
    """
    turns = QUARTER_TURNS_CW[build_dir]
    if turns == 0 or '[' not in block:
        return block

    new_dirs = RELATIVE_ROTATIONS[build_dir]
    name, state = block.split('[', 1)
    properties = []
    for prop in state.rstrip(']').split(','):
        if not prop:
            # Blocks without any state were serialized with empty brackets, e.g. air[]
            continue
        key, value = prop.split('=', 1)
        if key == "facing" and value in new_dirs:
            value = new_dirs[value]
        elif key in new_dirs:
            key = new_dirs[key]
        elif key == "axis" and value in ("x", "z") and turns % 2 == 1:
            value = "z" if value == "x" else "x"
        elif key == "rotation" and value.isdigit():
            # 4 steps of rotation is 90 degrees clockwise
            value = str((int(value) + 4 * turns) % 16)
        properties.append("{}={}".format(key, value))

    return "{}[{}]".format(name, ",".join(properties))


def build_from_3d_array(data: np.array, corner: (int, int, int), build_dir: 'Direction' = Direction.EAST,
                        biome: 'biomeUtils.BiomeGroup' = biomeUtils.BiomeGroup.DEFAULT):
    """
    Builds a structure from a numpy array. If standing on corner looking in build_dir, the structure will grow forwards
    and to the right (and up).
    :param biome:
    :param data: 3d numpy array with x,z,y data
    :param corner: corner to start the build (0,0,0) in numpy array
    :param build_dir: the direction in which the "x" dir of the structure is
    :return: None, builds structure in minecraft world
    """
    # x z y
    arr_size = data.shape
    use_batching = Config().use_batching

    def rotate_coordinate_about_corner(coord: (int, int, int)) -> (int, int, int):
        """
        :param coord: world-space coordinate in x, y, z
        :return: rotated coordinate depending on build direction
        """
        sub_origin = (coord[0] - corner[0], coord[2] - corner[2])
        # No op if build_dir is EAST
        if build_dir == Direction.EAST:
            after_rot = sub_origin
        if build_dir == Direction.SOUTH:
            # 90 degrees CW rotation
            after_rot = -sub_origin[1], sub_origin[0]
        if build_dir == Direction.WEST:
            after_rot = -sub_origin[0], -sub_origin[1]
        if build_dir == Direction.NORTH:
            # 90 degrees CCW rotation
            after_rot = sub_origin[1], -sub_origin[0]

        return after_rot[0] + corner[0], coord[1], after_rot[1] + corner[2]

    for x in range(arr_size[0]):
        for z in range(arr_size[1]):
            for y in range(arr_size[2]):
                # change direction according to build_dir
                newBlock = rotate_block_state(data[x][z][y], build_dir)
                # Take the block and find if it needs to be updated for current biome
                newBlock = biomeUtils.get_biome_equivalent(newBlock, biome)
                # put the block in world-space
                world_space = tuple(map(lambda i, j: i + j, (x, y, z), corner))
                # rotate if not building east
                target = rotate_coordinate_about_corner(world_space)
                blockUtils.setBlock(*target, newBlock)
        print("done column {} of {}".format(x, arr_size[0]))

    if use_batching:
        interfaceUtils.sendBlocks()
