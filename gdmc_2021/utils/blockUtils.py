from enum import Enum

from config import Config
from http_utils import interfaceUtils

# Horizontal plane movements [X, Z]
# CARDINAL
EAST = [1, 0]
SOUTH = [0, 1]
WEST = [-1, 0]
NORTH = [0, -1]
CARDINAL = [EAST, SOUTH, WEST, NORTH]

# DIAGONAL
NORTHEAST = [1, -1]
NORTHWEST = [-1, -1]
SOUTHEAST = [1, 1]
SOUTHWEST = [-1, 1]
DIAGONAL = [NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST]

EIGHT_DIRECTIONAL = CARDINAL + DIAGONAL


def setBlock(x, y, z, block):
    """Place blocks or add them to batch."""
    if Config().use_batching:
        # add block to buffer, send once buffer has 100 items in it
        interfaceUtils.placeBlockBatched(x, y, z, block, 400)
    else:
        interfaceUtils.setBlock(x, y, z, block)


def heightAt(x, z, heightmap):
    """Access height using local coordinates."""
    # Warning:
    # Heightmap coordinates are not equal to world coordinates!
    try:
        height = heightmap[(x - Config().build_area_origin[0], z - Config().build_area_origin[1])]
        return height
    except IndexError as e:
        # FIXME: not sure why things are going out of bounds
        print(e)
        return 90


class BlockRotation(Enum):
    """
    Indicates the way the block is facing. If not specified
    the minecraft default value is 0 (SOUTH)
    """
    SOUTH = 0
    SOUTH_SOUTHWEST = 1
    SOUTHWEST = 2
    WEST_SOUTHWEST = 3
    WEST = 4
    WEST_NORTHWEST = 5
    NORTHWEST = 6
    NORTH_NORTHWEST = 7
    NORTH = 8
    NORTH_NORTHEAST = 9
    NORTHEAST = 10
    EAST_NORTHEAST = 11
    EAST = 12
    EAST_SOUTHEAST = 13
    SOUTHEAST = 14
    SOUTH_SOUTHEAST = 15


class Direction(Enum):
    """
    Represents an orthogonal direction in-game
    """
    EAST = 0  # Facing positive x
    SOUTH = 1  # Facing positive z
    WEST = 2  # Facing negative x
    NORTH = 3  # Facing negative z


def plot_direction_from_string(s: str) -> Direction:
    if s == "east":
        return Direction.EAST
    if s == "south":
        return Direction.SOUTH
    if s == "west":
        return Direction.WEST
    if s == "north":
        return Direction.NORTH
    # Shouldn't get here
    print("WARNING SHOULDN'T GET HERE")
    return Direction.EAST


def string_from_direction(d: 'Direction') -> str:
    if d == Direction.EAST:
        return "east"
    if d == Direction.SOUTH:
        return "south"
    if d == Direction.WEST:
        return "west"
    if d == Direction.NORTH:
        return "north"
    # Shouldn't get here
    print("WARNING SHOULDN'T GET HERE")
    return "east"


class Movements:

    @staticmethod
    def directionsFromBitmask(bitmask):
        # MSB -> LSB: E W S N NE NW SE SW
        directions = []
        if bitmask & 128 == 128:
            directions.append(EAST)
        if bitmask & 64 == 64:
            directions.append(WEST)
        if bitmask & 32 == 32:
            directions.append(SOUTH)
        if bitmask & 16:
            directions.append(NORTH)
        if bitmask & 8:
            directions.append(NORTHEAST)
        if bitmask & 4:
            directions.append(NORTHWEST)
        if bitmask & 2:
            directions.append(SOUTHEAST)
        if bitmask & 1:
            directions.append(SOUTHWEST)
        return directions

    @staticmethod
    def bitmaskFromDirections(directions: list):
        # MSB -> LSB: E W S N NE NW SE SW
        bm = 0
        for d in directions:
            if d == EAST:
                bm |= 128
            elif d == WEST:
                bm |= 64
            elif d == SOUTH:
                bm |= 32
            elif d == NORTH:
                bm |= 16
            elif d == NORTHEAST:
                bm |= 8
            elif d == NORTHWEST:
                bm |= 4
            elif d == SOUTHEAST:
                bm |= 2
            elif d == SOUTHWEST:
                bm |= 1
        return bm



