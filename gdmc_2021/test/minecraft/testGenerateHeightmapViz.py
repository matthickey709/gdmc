import unittest

from http_utils import interfaceUtils, mapUtils
from http_utils.worldLoader import WorldSlice


class TestGenerateHeightmapViz(unittest.TestCase):
    """
    Class containing "unit tests" for generating the different types of height maps and visualizing them.
    """

    def setUp(self) -> None:
        """
        Get the build area and determine area and world slice from this information.
        :return: None, sets area and worldSlice
        """
        buildArea = interfaceUtils.requestBuildArea()
        if buildArea == -1:
            self.fail("No build area specified.")
        x1 = buildArea["xFrom"]
        z1 = buildArea["zFrom"]
        x2 = buildArea["xTo"]
        z2 = buildArea["zTo"]
        self.area = (x1, z1, x2 - x1, z2 - z1)
        self.worldSlice = WorldSlice(self.area)

    def test_visualizeHeightmap_calcGoodHeightmap(self):
        heightmap = mapUtils.calcGoodHeightmap(self.worldSlice)
        mapUtils.visualize(heightmap, title="heightmap (calcGoodHeightmap())")

    def test_visualizeHeightmap_WorldSurface(self):
        heightmap = self.worldSlice.heightmaps["WORLD_SURFACE"]
        mapUtils.visualize(heightmap, title="heightmap (world surface)")

    def test_visualizeHeightmap_MotionBlocking(self):
        heightmap = self.worldSlice.heightmaps["MOTION_BLOCKING"]
        mapUtils.visualize(heightmap, title="heightmap (motion blocking)")

    def test_visualizeHeightmap_MotionBlockingNoLeaves(self):
        heightmap = self.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        mapUtils.visualize(heightmap, title="heightmap (motion blocking no leaves)")


if __name__ == '__main__':
    unittest.main()
