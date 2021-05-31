import numpy as np
from math import sqrt
from dataclasses import dataclass
from queue import PriorityQueue
import functools
import random

from config import Config
from http_utils import interfaceUtils, mapUtils
from http_utils.worldLoader import WorldSlice
from structures.utilities.lamp_post import LampPost
from utils import blockUtils
from utils.pathfinding.pathfinding_utils import intersects


class PathBuilder:
    """
    Class that builds a path/road in minecraft from one point to another that is walkable by a player.
    """

    def __init__(self, start: (int, int), goal: (int, int), world_slice: 'WorldSlice',
                 legal_actions: np.array, path_config: dict, build_in_minecraft: True):
        self.legal_actions = legal_actions
        # path options
        self.path_config = path_config
        self.path_width = path_config['path_width']

        self.world_slice = world_slice
        self.heightmap = mapUtils.calcGoodHeightmap(world_slice)
        # (x,z) coordinates of start and goal in Minecraft world coordinates
        self.world_start = start
        self.world_goal = goal
        # (x,z) coordinates of start and goal in local coordinates
        self.local_start = start[0] - Config().build_area_origin[0], start[1] - Config().build_area_origin[1]
        self.local_goal = goal[0] - Config().build_area_origin[0], goal[1] - Config().build_area_origin[1]

        # A* open and closed list
        self.open = PriorityQueue()
        self.open.put(ComparableNode(self.local_start, None, None, 0, self.heuristic(self.local_start, self.local_goal)))
        self.closed = np.full_like(self.heightmap, 0)

        # numpy array to store which coordinates will be part of the path in local coordinates.
        self.path = np.full_like(self.heightmap, 0)

        self.build_in_minecraft = build_in_minecraft

    def build_path(self):
        """
        Called from object owner to start the path generation process. Calls determine_path()
        to determine which blocks need to be placed for the path, then calls place_path() to generate
        the path in the minecraft world.
        :return:
        """
        print("Attempting to build path from {} to {}".format(self.world_start, self.world_goal))
        try:
            self.determine_path()
        except PathNotFoundError:
            print("Couldn't find a legal path from {} to {}, skipping this edge of MST!".format(self.world_start, self.world_goal))
        if self.build_in_minecraft:
            self.place_path()

    @staticmethod
    def heuristic(start: (int, int), goal: (int, int)) -> int:
        """
        Heuristic function for building path
        :param start: Starting grid coordinate (x, z)
        :param goal: Ending grid coordinate (x, z)
        :return: Heuristic value to determine next steps for pathfinding
        """
        dx = abs(start[0] - goal[0])
        dz = abs(start[1] - goal[1])
        D, D2 = 1, sqrt(2)
        return D * (dx + dz) + (D2 - 2 * D) * min(dx, dz)

    def determine_path(self):
        """
        An A* Pathfinding Algorithm to connect self.start with self.goal
        :return: None, calculates the path and stores in class. Raises PathNotFoundError if it cannot be done.
        """
        while True:
            if not self.open:
                # This is a failure.
                raise PathNotFoundError

            node = self.pop_min_f()
            coord = node.coordinate

            if self.isAtGoal(node):
                # Done. At goal.
                return
            if self.closed[coord[0]][coord[1]]:
                # already checked here.
                continue
            self.closed[coord[0]][coord[1]] = True

            # Check all the legal actions at this coordinate
            actions = blockUtils.Movements.directionsFromBitmask(self.legal_actions[coord[0]][coord[1]])
            for action in actions:
                rx = coord[0] + action[0]
                rz = coord[1] + action[1]
                if self.closed[rx][rz]:
                    # Already checked
                    continue
                rg = node.g + (Config().heuristic_base_cost_diag if bool(action[0]) and bool(action[1]) else Config().heuristic_base_cost)
                rh = self.heuristic(coord, self.local_goal)

                # Put the node in the queue
                self.open.put(ComparableNode((rx, rz), node, action, rg, rh))

    def place_path(self):
        for x in range(self.path.shape[0]):
            for z in range(self.path.shape[1]):
                if self.path[x][z] == 1:
                    world_xz = x + Config().build_area_origin[0], z + Config().build_area_origin[1]
                    world_coord = world_xz[0], blockUtils.heightAt(world_xz[0], world_xz[1], self.heightmap) - 1, world_xz[1]
                    # one last check to ensure no intersections of existing plots
                    if intersects(world_xz[0], world_xz[1], self.path_config['plots']):
                        continue
                    # Finally, place the block for the path in the Minecraft world
                    blockUtils.setBlock(world_coord[0], world_coord[1], world_coord[2], self.path_config['paving_block'])

                    # Clear above-ground obstacles for pathconfig.vert_clearance
                    for clear in range(1, self.path_config['vertical_clearance'] + 1):
                        blockUtils.setBlock(world_coord[0], world_coord[1] + clear, world_coord[2], "air")

                    # Check if a lamp post should go here
                    if self.should_spawn_lighting():
                        lamp = LampPost(world_coord[0], world_coord[1] + 1, world_coord[2])
                        lamp.build()

                    if self.should_spawn_golem():
                        interfaceUtils.spawnMob(world_coord[0], world_coord[1] + 1, world_coord[2], "iron_golem")

        if Config().use_batching:
            # we need to send any blocks remaining in the buffer
            interfaceUtils.sendBlocks()

    def should_spawn_lighting(self) -> bool:
        return self.path_config['lighting_spawn_rate'] > random.random()

    def should_spawn_golem(self):
        return self.path_config['golem_spawn_rate'] > random.random()

    def pop_min_f(self) -> 'ComparableNode':
        return self.open.get()

    def isAtGoal(self, node: 'ComparableNode') -> bool:
        if node.coordinate == self.local_goal:
            self.set_path(node)
            return True
        return False

    def set_path(self, node):
        while node is not None:
            coord = node.coordinate
            for x in range(max(coord[0] - self.path_width, 0), min(coord[0] + self.path_width + 1, len(self.path))):
                for z in range(max(coord[1] - self.path_width, 0), min(coord[1] + self.path_width + 1, len(self.path[coord[0]]))):
                    self.path[x][z] = 1
            node = node.parent


@dataclass
class AStarNode(object):
    coordinate: (int, int)
    parent: 'AStarNode'
    action: list[int]
    g: int
    h: int


@functools.total_ordering
class ComparableNode(AStarNode):
    """
    Just like AStarNode but overridden > and == operators
    so it can be used in a priority queue based on f = g+h
    """
    def __gt__(self, other):
        return self.g + self.h > other.g + other.h

    def __eq__(self, other):
        return self.g + self.h == other.g + other.h


class PathNotFoundError(Exception):
    """
    Raised when a path can't be found between 2 coordinates in a Minecraft world.
    """
    pass
