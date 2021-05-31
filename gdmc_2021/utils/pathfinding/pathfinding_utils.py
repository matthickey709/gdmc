from math import sqrt
import numpy as np
import heapq
from collections import defaultdict
from functools import lru_cache

from config import Config
from utils import blockUtils

from http_utils.worldLoader import WorldSlice


@lru_cache(maxsize=None)
def distance(n1, n2):
    """
    Calculates the distance between points
    :param n1: One node
    :param n2: Other node
    :return: distance
    """
    return sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)


def create_graph_from_coordinates(coordinates: list[(int, int)]) -> dict:
    """
    Takes a list of MC world coordinates and creates and returns an adjacency list
    :param coordinates: List of MC world coordinates. Strongly connected.
    :return:
    """
    print("Generating graph from {} coordinates...".format(len(coordinates)))
    n = len(coordinates)
    graph = defaultdict(dict)
    # Need to do the list for each coordinate
    for i in range(n):
        for neighbour in range(n):
            if neighbour == i:
                continue
            # Find the distance between neighbours
            # always make call with lowest indexed first for caching
            p = sorted([i, neighbour])
            graph[i][neighbour] = distance(coordinates[p[0]], coordinates[p[1]])

    return graph


def create_mst_from_graph(graph: dict, start: int = 0):
    """
    Function that takes an adjacency list and creates an MST.
    Implemented with this resource https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
    :param graph:
    :param start:
    :return:
    """
    print("Creating MST from graph...")
    mst = defaultdict(set)
    visited = {start}
    edges = [(cost, start, to) for to, cost in graph[start].items()]
    heapq.heapify(edges)
    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))
    return mst


def intersects(x_, z_, rects):
    # TODO: if the x,z point lies within any of the rects, return True, otherwise False
    # Each element in rects is of form (xStart, zStart, xLen, zLen)
    for rect in rects:
        # if (x_, z_) is within the bound [xStart -> xStart + xLen) and [zStart -> zStart + zLen) then it intersects
        xStart, xEnd = rect[0], rect[0] + rect[2]
        zStart, zEnd = rect[1], rect[1] + rect[3]
        if xStart <= x_ < xEnd and zStart <= z_ < zEnd:
            return True
    return False


def determine_legal_actions(world_slice: 'WorldSlice', building_lots: list) -> np.array:
    heightmap = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # use bitmask to determine legal actions
    legal_actions = np.full_like(heightmap, 0)

    def is_legal_action(x_, z_, action_):
        """
        Determine if starting at (x_,z_) and taking action_ is legal.
        :param x_: x-coordinate in world space
        :param z_: z-coordinate in world space
        :param action_: [x,z] motion where x,z is one of [-1,0,1]
        :return:
        """
        rx, rz = x_ + action_[0], z_ + action_[1]
        # make sure rx, rz is inside the build area
        if rx < Config().build_area_rect[0] \
                or rz < Config().build_area_rect[1] \
                or rx >= Config().build_area_rect[2] \
                or rz >= Config().build_area_rect[3]:
            return False
        # if it's on the grid, see if we can move this way as a player and ensure we aren't paving over building lots
        if intersects(rx, rz, building_lots):
            return False
        y = blockUtils.heightAt(x_, z_, heightmap)
        ry = blockUtils.heightAt(rx, rz, heightmap)
        return ry - 1 <= y <= ry + 1

    for x in range(heightmap.shape[0]):
        for z in range(heightmap.shape[1]):
            for action in blockUtils.EIGHT_DIRECTIONAL:
                if is_legal_action(x + Config().build_area_origin[0], z + Config().build_area_origin[1], action):
                    bm = blockUtils.Movements.bitmaskFromDirections([action])
                    legal_actions[x][z] |= bm
    return legal_actions


def graph_node_for_building_plot(plot_rect: (int, int, int, int), entrance_facing: 'blockUtils.Direction'):
    """
    Accepts a rectangular building lot, and the direction the entrance faces. Returns an (x,z) coordinate to use for
    pathfinding and road generation.
    :param plot_rect: (minx, minz, lenx, lenz)
    :param entrance_facing: Cardinal direction that the entrance faces
    :return: (x,z) coordinate of where to build the road for this plot
    """
    Dir = blockUtils.Direction
    x, z, len_x, len_z = plot_rect
    if entrance_facing == Dir.EAST:
        block = x + len_x, z + int(0.5 * len_z)
    elif entrance_facing == Dir.SOUTH:
        block = x + int(0.5 * len_x), z + len_z
    elif entrance_facing == Dir.WEST:
        block = x, z + int(0.5 * len_z)
    else:  # NORTH
        block = x + int(0.5 * len_x), z

    return block[0] + blockUtils.CARDINAL[entrance_facing.value][0], block[1] + blockUtils.CARDINAL[entrance_facing.value][1]
