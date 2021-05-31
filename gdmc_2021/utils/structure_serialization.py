import numpy as np
import re

from config import Config
from http_utils import interfaceUtils
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


def getBlock(x, y, z) -> str:
    return interfaceUtils.getBlockState(x, y, z)


def setBlock(blockCoord, block, use_batching=True):
    x, y, z = blockCoord
    if use_batching:
        interfaceUtils.placeBlockBatched(x, y, z, block, 200)
    else:
        interfaceUtils.setBlock(x, y, z, block)


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
    # TODO: Get from config
    use_batching = Config().use_batching

    new_dir_map = RELATIVE_ROTATIONS[build_dir]
    directions = ["north", "south", "east", "west"]

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
                block = data[x][z][y]
                # change direction according to build_dir
                facing = re.findall(r"facing=(?=(" + '|'.join(directions) + r"))", block)
                if facing:
                    newBlock = re.sub(facing[0], new_dir_map[facing[0]], block)
                else:
                    newBlock = block
                # Take the block and find if it needs to be updated for current biome
                newBlock = biomeUtils.get_biome_equivalent(newBlock, biome)
                # put the block in world-space
                world_space = tuple(map(lambda i, j: i + j, (x, y, z), corner))
                # rotate if not building east
                target = rotate_coordinate_about_corner(world_space)
                setBlock(target, newBlock, use_batching)
        print("done column {} of {}".format(x, arr_size[0]))

    if use_batching:
        interfaceUtils.sendBlocks()
