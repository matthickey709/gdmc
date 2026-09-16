import unittest

from http_utils import mapUtils
from http_utils.worldLoader import WorldSlice
from tests.helpers import minecraft_build_area_rect, requires_minecraft


@requires_minecraft
class TestGenerateHeightmapViz(unittest.TestCase):
    """
    Class containing "unit tests" for generating the different types of height maps and visualizing them.
    """

    def setUp(self) -> None:
        """
        Get the build area and determine area and world slice from this information.
        :return: None, sets area and worldSlice
        """
        self.area = minecraft_build_area_rect()
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
