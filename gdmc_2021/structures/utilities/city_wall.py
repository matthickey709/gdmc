from utils.blockUtils import setBlock


def build_city_wall(xFrom, xTo, zFrom, zTo, heightmap, perimeter_max, min_clearance=2):
    # TODO: Add an entrance, or load in something to act as entrance
    def heightAt(x, z):
        """Access height using local coordinates."""
        # Warning:
        # Heightmap coordinates are not equal to world coordinates!
        return heightmap[(x - xTo, z - zTo)]
    wall_material = "stone"
    end_height = perimeter_max + min_clearance
    for x in range(xFrom, xTo):
        z = zFrom
        start_height = heightAt(x, z)
        for y in range(start_height, end_height):
            setBlock(x, y, z, wall_material)
    for z in range(zFrom, zTo):
        x = xFrom
        start_height = heightAt(x, z)
        for y in range(start_height, end_height):
            setBlock(x, y, z, wall_material)
    for x in range(xFrom, xTo):
        z = zTo - 1
        start_height = heightAt(x, z)
        for y in range(start_height, end_height):
            setBlock(x, y, z, wall_material)
    for z in range(zFrom, zTo):
        x = xTo - 1
        start_height = heightAt(x, z)
        for y in range(start_height, end_height):
            setBlock(x, y, z, wall_material)