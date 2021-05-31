import unittest
from numpy.testing import assert_array_equal

import utils.structure_serialization
from config import Config
from utils.biomeUtils import BiomeGroup
from utils.blockUtils import Direction


class TestStructureSerialization(unittest.TestCase):

    def test_serialization(self):
        x = 6612, 6628
        z = -1312, -1296
        y = 3, 24
        filename = "../../../structures/houses/skinnyHouse.gz"
        data = utils.structure_serialization.serialize_rect_prism((x[0], z[0]), (x[1], z[1]), y[0], y[1])
        utils.structure_serialization.save_3d_to_file(filename, data)
        loaded = utils.structure_serialization.reload_3d_from_file(filename, data.shape[2])
        assert_array_equal(data, loaded)

    def test_build_from_file(self):
        corner = (6595, 3, -1257)
        filename = "../../../structures/houses/skinnyHouse.gz"
        data = utils.structure_serialization.reload_3d_from_file(filename, Config().structures["skinny_house"]["scaling_factor"])
        utils.structure_serialization.build_from_3d_array(data, corner, build_dir=Direction.SOUTH, biome=BiomeGroup.BADLANDS)



if __name__ == '__main__':
    unittest.main()
