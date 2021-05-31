import unittest
from GDMCSettlementGenerator import GDMCSettlementGenerator
from utils.blockUtils import Direction


class OrientationTests(unittest.TestCase):

    # TEST MIDDLE DIRECTION TESTS
    def test_middle_east1(self):
        area = (50, 100, 100, 300)
        x, z = 60, 150
        direction = GDMCSettlementGenerator.get_middle_direction(x, z, area)
        self.assertEqual(Direction.EAST, direction)

    def test_middle_north1(self):
        area = (50, 100, 100, 300)
        x, z = 100, 300
        direction = GDMCSettlementGenerator.get_middle_direction(x, z, area)
        self.assertEqual(Direction.NORTH, direction)

    def test_middle_west1(self):
        area = (50, 100, 100, 300)
        x, z = 140, 150
        direction = GDMCSettlementGenerator.get_middle_direction(x, z, area)
        self.assertEqual(Direction.WEST, direction)

    def test_middle_south1(self):
        area = (50, 100, 100, 300)
        x, z = 140, 105
        direction = GDMCSettlementGenerator.get_middle_direction(x, z, area)
        self.assertEqual(Direction.SOUTH, direction)

    # TEST ENTRANCE FACING --> BUILD DIRECTION TESTS
    def test_high_class_home(self):
        # the entrance is facing north in the default east direction
        struct = "high_class_home"
        entrance_goals = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]
        build_dir_goals = [Direction.SOUTH, Direction.WEST, Direction.NORTH, Direction.EAST]
        for i in range(len(entrance_goals)):
            build_dir = GDMCSettlementGenerator.get_build_direction(struct, entrance_goals[i])
            self.assertEqual(build_dir_goals[i], build_dir)


if __name__ == '__main__':
    unittest.main()
