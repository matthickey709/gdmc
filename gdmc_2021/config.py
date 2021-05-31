from math import sqrt
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STRUCTURES_CONFIG = os.path.join(ROOT_DIR, "structures", "structures.json")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    use_batching: bool
    overall_timeout: int

    def __init__(self):
        self.use_batching = True
        self.overall_timeout = 10*60  # 10 mins for the program to run
        self.world_slice_timeout = 4*60  # 4 mins
        self.heuristic_base_cost = 100
        self.heuristic_base_cost_diag = round(sqrt(self.heuristic_base_cost**2 * 2))
        with open(STRUCTURES_CONFIG) as json_file:
            self.structures = json.load(json_file)
        # Delete the unwanted structures
        del self.structures['redstone_hotel']  # too enormous
        del self.structures['cabin_with_small_lake']  # water is buggy
        del self.structures['double_watchtower']  # too large and buggy
        del self.structures['modern_home']  # too many strange materials that are just for show
        del self.structures['high_class_home']
        self.build_area_origin = (0, 0)
        self.build_area_rect = (0, 0, 0, 0)
        self.force_biome = False
        self.forced_biome = None
        self.overlap_border = 5

    def set_build_area_origin(self, x, z):
        self.build_area_origin = x, z

    def set_build_area_rect(self, xFrom, zFrom, xTo, zTo):
        self.build_area_rect = (xFrom, zFrom, xTo, zTo)
