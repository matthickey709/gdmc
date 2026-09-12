import gzip
import json
import os
import unittest

from config import ROOT_DIR, STRUCTURES_CONFIG


class TestStructuresConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Read the file directly: Config() removes the structures that aren't used
        with open(STRUCTURES_CONFIG) as json_file:
            cls.structures = json.load(json_file)

    def test_dimensions_match_structure_files(self):
        for name, struct in self.structures.items():
            with self.subTest(structure=name):
                path = os.path.join(ROOT_DIR, "structures", struct["build_type"], struct["filename"])
                with gzip.open(path, "rt") as structure_file:
                    # One row per x, holding z * height blocks
                    row_lengths = {len(line.split()) for line in structure_file}
                    structure_file.seek(0)
                    rows = sum(1 for _ in structure_file)

                self.assertEqual(struct["length"], rows)
                self.assertEqual({struct["width"] * struct["scaling_factor"]}, row_lengths)

    def test_entrance_faces_a_cardinal_direction(self):
        for name, struct in self.structures.items():
            with self.subTest(structure=name):
                self.assertIn(struct["entrance_facing"], {"north", "east", "south", "west"})


if __name__ == '__main__':
    unittest.main()
