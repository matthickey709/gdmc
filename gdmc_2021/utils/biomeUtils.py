"""
Right now there isn't an easy way to get biome info out of the world slice.
However the people on the discord seem to think it's alright if you just sample
some blocks and make a decision.
"""
import re
from enum import Enum
from collections import Counter

from http_utils.worldLoader import WorldSlice
from utils.blockUtils import Direction

DEFAULT_BIOMES = {
    1,
    4,
    5,
    8,
    9,
    14,
    15,
    18,
    19,
    27,
    28,
    29,
    32,
    33,
    34,
    35,
    36,
    40,
    41,
    42,
    43,
    127,
    129,
    132,
    133,
    155,
    156,
    157,
    160,
    161,
    163,
    164,
    170,
    171,
    172,
    173
}

SNOW_BIOMES = {
    12,
    13,
    26,
    30,
    31,
    140,
    158
}
TROPICAL_BIOMES = {
    21,
    22,
    23,
    149,
    151,
    168,
    169
}
COLD_BIOMES = {}
WARM_BIOMES = {
    2,
    16,
    17
}
OCEAN_BIOMES = {
    0,
    10,
    24,
    44,
    45,
    46,
    47,
    48,
    49,
    50
}
RUGGED_BIOMES = {
    3,
    20,
    25,
    131,
    162
}
RUNNING_WATER_BIOMES = {
    6,
    7,
    11,
    130,
    134
}
BADLANDS_BIOMES = {
    37,
    38,
    39,
    165,
    166,
    167
}


class BiomeGroup(Enum):
    """
    Logical grouping of biomes. With inspiration from "Settlement Generation in Minecraft"
    by Marcus Fridh and Fredrik Sy, Malmo Universitet, 2020
    """
    SNOW = 0  # places with snow on the ground
    COLD = 1  # places that may be cold, but not snowy
    TROPICAL = 2  # jungle
    WARM = 3  # warm but not full of lots of vegetation, like deserts
    OCEAN = 4  # self explanatory
    RUGGED = 5  # mountains and other stone-filled terrains
    RUNNING_WATER = 6  # Like rivers
    DEFAULT = 7
    BADLANDS = 8  # needs to be differentiated from normal sandy deserts


BIOME_LOOKUP = {
    "grass_block": {
        BiomeGroup.SNOW: "snow_block",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "sandstone",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: None,
        BiomeGroup.RUNNING_WATER: "oak_planks",
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "dirt": {
        BiomeGroup.SNOW: "snow_block",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "sandstone",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: None,
        BiomeGroup.RUNNING_WATER: "oak_planks",
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "coarse_dirt": {
        BiomeGroup.SNOW: "snow_block",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "sand",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: None,
        BiomeGroup.RUNNING_WATER: "oak_planks",
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "stone": {
        BiomeGroup.SNOW: None,
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "smooth_sandstone",
        BiomeGroup.OCEAN: None,
        BiomeGroup.RUGGED: None,
        BiomeGroup.TROPICAL: "jungle_log",  # Maybe keep as stone?
        BiomeGroup.RUNNING_WATER: None,
        BiomeGroup.BADLANDS: "red_terracotta",
        BiomeGroup.DEFAULT: None
    },
    "polished_andesite": {
        BiomeGroup.SNOW: None,
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "smooth_sandstone",
        BiomeGroup.OCEAN: None,
        BiomeGroup.RUGGED: None,
        BiomeGroup.TROPICAL: "jungle_log",
        BiomeGroup.RUNNING_WATER: None,
        BiomeGroup.BADLANDS: "smooth_red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "stone_bricks": {
        BiomeGroup.SNOW: None,
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "smooth_sandstone",
        BiomeGroup.OCEAN: None,
        BiomeGroup.RUGGED: None,
        BiomeGroup.TROPICAL: "jungle_log",  # Maybe keep as stone?
        BiomeGroup.RUNNING_WATER: None,
        BiomeGroup.BADLANDS: "chiseled_red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "cobblestone": {
        BiomeGroup.SNOW: None,
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "smooth_sandstone",
        BiomeGroup.OCEAN: None,
        BiomeGroup.RUGGED: None,
        BiomeGroup.TROPICAL: "jungle_log",  # Maybe keep as stone?
        BiomeGroup.RUNNING_WATER: None,
        BiomeGroup.BADLANDS: "light_gray_terracotta",
        BiomeGroup.DEFAULT: None
    },
    "sand": {
        BiomeGroup.SNOW: "snow_block",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "sandstone",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: "grass_block",  # Maybe jungle_planks?
        BiomeGroup.RUNNING_WATER: "warped_planks",  # Maybe spruce_planks?
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: "grass_block"
    },
    "gravel": {
        BiomeGroup.SNOW: "snow_block",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: "sandstone",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "cobblestone",
        BiomeGroup.TROPICAL: "grass_block",
        BiomeGroup.RUNNING_WATER: "warped_planks",
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: "grass_block"
    },
    "sandstone": {
        BiomeGroup.SNOW: "granite",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: None,
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: "stripped_jungle_wood",
        BiomeGroup.RUNNING_WATER: "oak_planks",  # Maybe spruce_planks?
        BiomeGroup.BADLANDS: "red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "smooth_sandstone": {
        BiomeGroup.SNOW: "granite",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: None,
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: "stripped_jungle_wood",
        BiomeGroup.RUNNING_WATER: "oak_planks",  # Maybe spruce_planks?
        BiomeGroup.BADLANDS: "smooth_red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "cut_sandstone": {
        BiomeGroup.SNOW: "granite",
        BiomeGroup.COLD: None,
        BiomeGroup.WARM: None,
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "stone",
        BiomeGroup.TROPICAL: "stripped_jungle_wood",
        BiomeGroup.RUNNING_WATER: "oak_planks",  # Maybe spruce_planks?
        BiomeGroup.BADLANDS: "cut_red_sandstone",
        BiomeGroup.DEFAULT: None
    },
    "scaffolding": {  # can't trust this
        BiomeGroup.SNOW: "oak_planks",
        BiomeGroup.COLD: "oak_planks",
        BiomeGroup.WARM: "oak_planks",
        BiomeGroup.OCEAN: "oak_planks",
        BiomeGroup.RUGGED: "oak_planks",
        BiomeGroup.TROPICAL: "oak_planks",
        BiomeGroup.RUNNING_WATER: "oak_planks",
        BiomeGroup.BADLANDS: "oak_planks",
        BiomeGroup.DEFAULT: "oak_planks"
    }

}


def get_biome_group(biomeId: int) -> 'BiomeGroup':
    """
    TODO: Given a biome number, assign it a group
    that is one of the BiomeGroups.
    """
    if biomeId in SNOW_BIOMES:
        return BiomeGroup.SNOW
    if biomeId in COLD_BIOMES:
        return BiomeGroup.COLD
    if biomeId in TROPICAL_BIOMES:
        return BiomeGroup.TROPICAL
    if biomeId in WARM_BIOMES:
        return BiomeGroup.WARM
    if biomeId in OCEAN_BIOMES:
        return BiomeGroup.OCEAN
    if biomeId in RUGGED_BIOMES:
        return BiomeGroup.RUGGED
    if biomeId in RUNNING_WATER_BIOMES:
        return BiomeGroup.RUNNING_WATER
    if biomeId in BADLANDS_BIOMES:
        return BiomeGroup.BADLANDS
    return BiomeGroup.DEFAULT


def get_biome_equivalent(block: str, destination: 'BiomeGroup') -> str:
    """
    Given a minecraft block and a destination biome, lookup it's equivalent in that biome if it exists
    :param block: text id of the minecraft block
    :param destination: the BiomeGroup of where this block is going
    :return: The block that should be placed to reflect the biome
    """

    # TODO: Handle the blocks with state information
    # Separate the state information from the block. [0] is block, [1] is state without leading '['
    info = block.split('[')
    search = info[0]
    try:
        lookup = BIOME_LOOKUP[search][destination]
        if lookup is None:
            # If what we're looking for isn't there just keep it the way it was
            return block
    except KeyError:
        # If what we're looking for isn't there just keep it the way it was
        return block

    if re.search(r"facing", block):
        # Need to append the state info
        return '['.join([lookup] + info[1:])
    else:
        return lookup


def calculate_prevalent_biome_group(rect: (int, int, int, int), world_slice: 'WorldSlice', direction: 'Direction') -> 'BiomeGroup':
    c = Counter()
    STEP_SIZE = 4
    X_DIR, Z_DIR = 1, 1
    y = 150  # I don't think it matters what height you're checking as long as it isn't in the void
    if direction == Direction.EAST:
        x_target, z_target = rect[0] + rect[2], rect[1] + rect[3]
    elif direction == Direction.SOUTH:
        X_DIR = -X_DIR
        x_target, z_target = rect[0] - rect[3], rect[1] + rect[2]
    elif direction == Direction.WEST:
        X_DIR, Z_DIR = -X_DIR, -Z_DIR
        x_target, z_target = rect[0] - rect[2], rect[1] - rect[3]
    elif direction == Direction.NORTH:
        Z_DIR = -Z_DIR
        x_target, z_target = rect[0] + rect[3], rect[1] - rect[2]

    for x in range(rect[0], x_target, X_DIR * STEP_SIZE):
        for z in range(rect[1], z_target, Z_DIR * STEP_SIZE):
            biome = world_slice.getBiomeAt((x, y, z))
            c[biome] += 1
    prevalent_biome = c.most_common(1)[0][0]
    biome_group = get_biome_group(prevalent_biome)
    print("Found most common biome to be {}. Returning biome group: {}".format(prevalent_biome, biome_group))
    return biome_group
