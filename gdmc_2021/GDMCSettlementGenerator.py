"""
This is the file that contains the actual settlement generator.
"""

from multiprocessing import Process
import os
import time
import random
import statistics
import numpy as np

from config import Config, ROOT_DIR
from http_utils import interfaceUtils, mapUtils
from http_utils.worldLoader import WorldSlice
import utils.structure_serialization
from utils import blockUtils
from utils.blockUtils import Direction, plot_direction_from_string, string_from_direction, heightAt
from utils import structure, biomeUtils
from utils.pathfinding import pathfinding_utils
from utils.pathfinding.path_builder import PathBuilder

CONFIG = Config()


class GDMCSettlementGenerator:
    """
    Will generate a minecraft settlement
    """

    def __init__(self, build_area: dict = None):
        """
        :param build_area: represents the build area. If not specified it is requested from Minecraft. Needs to be a
            dict with the keys xFrom, zFrom, xTo and zTo.
        :return: Instance of GDMCSettlementGenerator
        """
        # TODO: Take in the biome stuff, but config defaults it to not force biome
        # Find the area for building
        self.AREA = None
        self.determine_build_area(build_area=build_area)
        # Retrieve world slice including heightmaps
        world_loading = time.time()
        self.WORLD_SLICE = WorldSlice(self.AREA)
        print("Generated world slice in {}s".format(time.time() - world_loading))

        self.building_plots = []
        self.HEIGHTMAP = mapUtils.calcGoodHeightmap(self.WORLD_SLICE)
        self.pathfinding_points = []
        self.debug = False
        self.build_roads = True

    def determine_build_area(self, build_area) -> None:
        """
        Determine the x,z starting coordinate and set self.AREA to the appropriate value.
        :param build_area: supplied build_area. May be None
        :return: None, sets self.AREA
        """
        bld_area = build_area if build_area is not None else interfaceUtils.requestBuildArea()
        if bld_area == -1 or not all(k in bld_area for k in ("xFrom", "zFrom", "xTo", "zTo")):
            # Build area not specified or invalid
            raise ValueError("Empty or invalid build area specified")
        x1 = bld_area["xFrom"]
        z1 = bld_area["zFrom"]
        x2 = bld_area["xTo"]
        z2 = bld_area["zTo"]
        self.AREA = (x1, z1, x2 - x1, z2 - z1)
        Config().set_build_area_origin(x1, z1)
        Config().set_build_area_rect(bld_area["xFrom"], bld_area["zFrom"], bld_area["xTo"], bld_area["zTo"])
        assert self.AREA is not None

    def setBlock(self, x, y, z, block):
        """Place blocks or add them to batch."""
        blockUtils.setBlock(x, y, z, block)

    def build_from_file(self, x, y, z, structName, direction):
        corner = (x, y, z)
        struct = Config().structures[structName]
        filename = os.path.join(ROOT_DIR, "structures", struct["build_type"], struct["filename"])
        data = utils.structure_serialization.reload_3d_from_file(filename, struct["scaling_factor"])

        if Config().force_biome:
            biome = Config().forced_biome
        else:
            biome = biomeUtils.calculate_prevalent_biome_group((x, z, data.shape[0], data.shape[1]), self.WORLD_SLICE, direction)
        utils.structure_serialization.build_from_3d_array(data, corner, build_dir=direction, biome=biome)

    def spawn_villagers(self, plot):
        x,z = 0, 0
        if plot.direction == Direction.EAST:
            x = plot.r[0] + plot.r[2]
            z = plot.r[1] + plot.r[3]/2
        if plot.direction == Direction.WEST:
            x = plot.r[0]
            z = plot.r[1] + plot.r[3]/2
        if plot.direction == Direction.SOUTH:
            x = plot.r[0] + plot.r[2]/2
            z = plot.r[1] + plot.r[3]
        if plot.direction == Direction.NORTH:
            x = plot.r[0] + plot.r[2]/2
            z = plot.r[1]

        y = heightAt(int(x), int(z), self.HEIGHTMAP)
        numvillagers = (random.random())**2 * 5
        for i in range (int(numvillagers)):
            interfaceUtils.spawnMob(x, y, z, "villager")

    def check_overlap(self, structure):
        for s in self.building_plots:
            if structure.overlap(s, Config().overlap_border):
                return True
        return False

    def get_plot_flatness(self, structure):
        """
        :param structure: plot that lies inside the build area
        :return: (flatness score, where 1 is flat and larger is bumpier, based on the plot's four corners;
            median height of the plot)
        """
        xmin = structure.r[0]
        xmax = structure.r[0] + structure.r[2] - 1
        zmin = structure.r[1]
        zmax = structure.r[1] + structure.r[3] - 1

        origin_x, origin_z = Config().build_area_origin
        footprint = self.HEIGHTMAP[xmin - origin_x:xmax - origin_x + 1, zmin - origin_z:zmax - origin_z + 1]
        corners = [heightAt(xmin, zmin, self.HEIGHTMAP), heightAt(xmin, zmax, self.HEIGHTMAP),
                   heightAt(xmax, zmin, self.HEIGHTMAP), heightAt(xmax, zmax, self.HEIGHTMAP)]

        return (statistics.stdev(corners) + 1) ** 3, int(np.median(footprint))

    @staticmethod
    def get_build_direction(struct_name: str, goal_direction: Direction) -> Direction:
        # goal direction is the way we want the entrance to face.

        structure_entrance_facing: str = Config().structures[struct_name]["entrance_facing"]
        structure_entrance_facing_dir = plot_direction_from_string(structure_entrance_facing)

        # If the way the entrance is facing is the way we already want, then return EAST because it's the way
        # the structure was serialized, so it will come out facing the desired way.
        if structure_entrance_facing_dir == goal_direction:
            return Direction.EAST

        # The entrance of the structure is not the goal direction. Need to find out how to orient the build direction
        #   so that the entrance faces the goal_direction.
        goal_direction_str = string_from_direction(goal_direction)
        rel_rots = utils.structure_serialization.RELATIVE_ROTATIONS
        # return the key where structure : desired
        for k, sub in rel_rots.items():
            if sub[structure_entrance_facing] == goal_direction_str:
                return k

        # If we got to here something went wrong, just default to east
        print("Error determining build direction. Defaulting to EAST")
        return Direction.EAST

    @staticmethod
    def get_middle_direction(x, z, area) -> 'Direction':
        x_start, z_start, x_len, z_len = area
        m = x_len / z_len
        pos_diag_x = m * z + x_start - m * z_start
        neg_diag_x = -m * z + x_start + m * (z_start + z_len)

        if pos_diag_x <= x < neg_diag_x:
            # Greater than positive line, less than negative line
            return Direction.SOUTH
        if neg_diag_x <= x < pos_diag_x:
            # Greater than negative line, less than positive line
            return Direction.NORTH
        if x >= pos_diag_x and x >= neg_diag_x:
            # Greater than both lines, doesn't matter which line is greater
            return Direction.WEST
        if x <= pos_diag_x and x <= neg_diag_x:
            return Direction.EAST

        print("Unexpected behaviour determining direction to middle. Defaulting to east.")
        return Direction.EAST

    @staticmethod
    def build_origin_for_plot(x: int, z: int, length: int, width: int, build_direction: Direction) -> (int, int):
        """
        build_from_3d_array rotates a structure about the corner it is given, so unless the structure is built EAST
        that corner isn't the plot's lowest (x, z). Finds the corner that makes the built structure cover exactly the
        plot [x, x + length) by [z, z + width).
        :param length: plot size along x, already swapped with width for NORTH/SOUTH builds
        :param width: plot size along z, already swapped with length for NORTH/SOUTH builds
        :return: (x, z) corner to pass to build_from_3d_array
        """
        if build_direction == Direction.SOUTH:
            return x + length - 1, z
        if build_direction == Direction.WEST:
            return x + length - 1, z + width - 1
        if build_direction == Direction.NORTH:
            return x, z + width - 1
        return x, z

    @staticmethod
    def perimeter_coordinates(area: (int, int, int, int)):
        """
        :param area: (x start, z start, x length, z length)
        :return: generator over each (x, z) coordinate on the edge of area, once each
        """
        xs, zs, xl, zl = area
        for x in range(xs, xs + xl):
            yield x, zs
            yield x, zs + zl - 1
        for z in range(zs + 1, zs + zl - 1):
            yield xs, z
            yield xs + xl - 1, z

    @staticmethod
    def should_build_fence(x: int, z: int, area: (int, int, int, int), opening_denominator: int = 5) -> bool:
        """
        The perimeter fence is left open in the middle 1/opening_denominator of each side to make a gate.
        :param x: x coordinate on the perimeter of area
        :param z: z coordinate on the perimeter of area
        :param area: (x start, z start, x length, z length)
        :return: False if (x, z) is part of a gate
        """
        xs, zs, xl, zl = area
        fenced_fraction = (opening_denominator // 2) / opening_denominator
        in_x_opening = xs + fenced_fraction * xl <= x < xs + xl - fenced_fraction * xl
        in_z_opening = zs + fenced_fraction * zl <= z < zs + zl - fenced_fraction * zl
        on_north_or_south_edge = z == zs or z == zs + zl - 1
        on_west_or_east_edge = x == xs or x == xs + xl - 1
        return not ((on_north_or_south_edge and in_x_opening) or (on_west_or_east_edge and in_z_opening))

    @staticmethod
    def area_inside_fence(area: (int, int, int, int)) -> (int, int, int, int):
        return area[0] + 1, area[1] + 1, area[2] - 2, area[3] - 2

    def generate_settlement(self) -> None:

        structureNames = list(Config().structures.keys())

        print("Beginning settlement generation...")
        print("Build area is at position {}, {} with size {}, {}".format(*self.AREA))
        # build a fence along the perimeter with access points in the middle for a fifth of the length/width
        for x, z in self.perimeter_coordinates(self.AREA):
            y = heightAt(x, z, self.HEIGHTMAP)
            self.setBlock(x, y - 1, z, "cobblestone")
            if self.should_build_fence(x, z, self.AREA):
                self.setBlock(x, y, z, "oak_fence")

        area_in_fence = self.area_inside_fence(self.AREA)
        print("AREA: {}, area_in_fence: {}".format(self.AREA, area_in_fence))

        print("Generating structures...")
        for x in range(area_in_fence[0], area_in_fence[0] + area_in_fence[2]):
            for z in range(area_in_fence[1], area_in_fence[1] + area_in_fence[3]):
                # Pick a random structure that will go on this potential plot
                struct = structureNames[random.randint(0, len(structureNames) - 1)]
                # middle_direction is the way that the entrance should face when the structure is built
                middle_direction = self.get_middle_direction(x, z, area_in_fence)
                # build_direction is the argument passed to the build function to ensure the entrance is facing correct
                build_direction = self.get_build_direction(struct, middle_direction)
                # length is along the x axis w.r.t. how it was serialized. width along the z
                length, width = Config().structures[struct]["length"], Config().structures[struct]["width"]
                if build_direction == Direction.NORTH or build_direction == Direction.SOUTH:
                    length, width = width, length
                genx, genz = self.build_origin_for_plot(x, z, length, width, build_direction)

                plot = structure.Structure(x, z, length, width, middle_direction)
                # If the plot is inside the fence and doesn't overlap with another one
                if plot.isInBuildArea(area_in_fence) and not self.check_overlap(plot):
                    plot_flatness, plot_height = self.get_plot_flatness(plot)
                    if Config().structures[struct]["weight"] * 0.05 / plot_flatness > random.random():
                        print("building structure {}".format(struct))
                        print(" Building dimensions:")
                        print(plot.r)
                        print(genx, genz)
                        self.build_from_file(genx, plot_height - 1, genz, struct,
                                             build_direction)
                        self.spawn_villagers(plot)
                        self.building_plots.append(plot)

        """
        Generate a list of points at each of the structures to use as a graph node for Prim's algorithm and pathfinding
        """
        for plot in self.building_plots:
            node = pathfinding_utils.graph_node_for_building_plot(plot.r, plot.direction)
            if self.point_contained_in(node, self.AREA):
                self.pathfinding_points.append(node)
            else:
                print("Road node {} for plot {} is outside the build area, leaving it off the road network".format(node, plot.r))

        if self.build_roads and len(self.pathfinding_points) >= 2:
            plots = [plot.r for plot in self.building_plots]
            graph = dict(pathfinding_utils.create_graph_from_coordinates(self.pathfinding_points))
            print("Generating MST of structures in the settlement")
            mst = dict(pathfinding_utils.create_mst_from_graph(graph))
            print("Determining legal actions for build area")
            legal_actions = pathfinding_utils.determine_legal_actions(self.WORLD_SLICE, plots)
            path_config = {
                'path_width': 1,
                'paving_block': 'black_concrete',
                'bridge_block': 'oak_planks',
                'plots': plots,
                'vertical_clearance': 5,
                'lighting_spawn_rate': 0.01,
                'golem_spawn_rate' : 0.0005
            }
            if self.debug:
                print("Pathfinding nodes: {}".format(self.pathfinding_points))

            # Find and place each road before moving on to the next, so roads finished before the timeout are kept
            for node in mst.keys():
                for neighbour in list(mst[node]):
                    builder = PathBuilder(start=self.pathfinding_points[node], goal=self.pathfinding_points[neighbour],
                                          world_slice=self.WORLD_SLICE, legal_actions=legal_actions,
                                          path_config=path_config, build_in_minecraft=True)
                    builder.build_path()

        if Config().use_batching:
            # push out any blocks remaining in the buffer, e.g. the fence if no structures were built
            interfaceUtils.sendBlocks()

    @staticmethod
    def point_contained_in(point: (int, int), area: (int, int, int, int)) -> bool:
        x, z = point
        return area[0] <= x < area[0] + area[2] and area[1] <= z < area[1] + area[3]


def main():
    """
    Main function for generating a settlement in Minecraft. Will time out after 10 minutes
    as per competition guidelines.
    :return: None
    """
    generator = GDMCSettlementGenerator()
    generator.generate_settlement()


if __name__ == "__main__":
    print("Enter the timeout in minutes for the settlement generator.")
    timeout_in_minutes = input("Leave blank for default of 10 minutes: ")
    if timeout_in_minutes is None or timeout_in_minutes == "":
        timeout_in_minutes = 10
    timeout_in_minutes = int(timeout_in_minutes)
    timeout_in_seconds = 60 * timeout_in_minutes
    print("Beginning generation with a timeout of {} minutes...".format(timeout_in_minutes))
    start = time.time()
    # Generation runs in its own process so it can be stopped at the time limit. That process sends its blocks to
    # Minecraft as each structure and road is finished; anything still in its buffer when it is stopped is lost.
    main_process = Process(target=main)
    main_process.start()
    main_process.join(timeout=timeout_in_seconds)
    if main_process.is_alive():
        print("Timeout reached, stopping settlement generation")
        main_process.terminate()
    print("Finished settlement generation in {}s ({}mins)".format(time.time() - start, (time.time() - start)/60))
