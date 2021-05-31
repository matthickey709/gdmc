import unittest
from utils.structure import Structure


class BuildAreaBoundingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.build_area = (0, 0, 256, 256)

    def test_completely_bounded(self):
        plot = (1, 1, 100, 100)
        struct = Structure(*plot, "test")

        self.assertEqual(True, struct.isInBuildArea(self.build_area))

    def test_completely_outside(self):
        plot = (256, 256, 10, 10)
        struct = Structure(*plot, "test")

        self.assertEqual(False, struct.isInBuildArea(self.build_area))

    def test_bottom_left_in_top_right_out(self):
        plot = (230, 230, 100, 100)
        struct = Structure(*plot, "test")

        self.assertEqual(False, struct.isInBuildArea(self.build_area))

    def test_top_right_in_bottom_left_out(self):
        plot = (-15, -15, 100, 100)
        struct = Structure(*plot, "test")

        self.assertEqual(False, struct.isInBuildArea(self.build_area))


if __name__ == '__main__':
    unittest.main()
