import os
import tempfile
import unittest
from numpy.testing import assert_array_equal

import utils.structure_serialization
from config import Config, ROOT_DIR
from tests.helpers import MINECRAFT_BUILD_AREA, requires_minecraft
from utils.biomeUtils import BiomeGroup
from utils.blockUtils import Direction


@requires_minecraft
class TestStructureSerialization(unittest.TestCase):

    def setUp(self) -> None:
        self.x, self.y, self.z = MINECRAFT_BUILD_AREA["xFrom"], MINECRAFT_BUILD_AREA["yFrom"], MINECRAFT_BUILD_AREA["zFrom"]

    def test_serialization(self):
        data = utils.structure_serialization.serialize_rect_prism((self.x, self.z), (self.x + 4, self.z + 4), self.y, self.y + 4)
        # Save somewhere temporary, so the structures that ship with the generator aren't overwritten
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "structure.gz")
            utils.structure_serialization.save_3d_to_file(filename, data)
            loaded = utils.structure_serialization.reload_3d_from_file(filename, data.shape[2])
        assert_array_equal(data, loaded)

    def test_build_from_file(self):
        struct = Config().structures["skinny_house"]
        filename = os.path.join(ROOT_DIR, "structures", struct["build_type"], struct["filename"])
        data = utils.structure_serialization.reload_3d_from_file(filename, struct["scaling_factor"])
        # Building SOUTH rotates the structure towards -x from its corner, so start far enough in to stay in the build area
        corner = (self.x + struct["width"] - 1, self.y, self.z)
        utils.structure_serialization.build_from_3d_array(data, corner, build_dir=Direction.SOUTH, biome=BiomeGroup.BADLANDS)


if __name__ == '__main__':
    unittest.main()
