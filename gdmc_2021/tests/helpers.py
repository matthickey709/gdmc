"""
Shared helpers for the test suite.
"""
import unittest

import requests

from config import Config

GDMC_HTTP_URL = "http://localhost:9000"


def _request_build_area():
    """
    :return: the build area dict from the GDMC HTTP mod, or None if Minecraft isn't reachable or has no build area
    """
    try:
        response = requests.get(GDMC_HTTP_URL + "/buildarea", timeout=1)
    except requests.exceptions.RequestException:
        return None
    return response.json() if response.ok else None


MINECRAFT_BUILD_AREA = _request_build_area()

# For tests that need Minecraft running with the GDMC HTTP mod and a build area set.
requires_minecraft = unittest.skipIf(MINECRAFT_BUILD_AREA is None,
                                     "needs Minecraft running with the GDMC HTTP mod and a build area set")


def minecraft_build_area_rect() -> (int, int, int, int):
    """
    :return: (x start, z start, x length, z length) of the build area set in Minecraft
    """
    area = MINECRAFT_BUILD_AREA
    return area["xFrom"], area["zFrom"], area["xTo"] - area["xFrom"], area["zTo"] - area["zFrom"]


def set_build_area(x: int, z: int, x_length: int, z_length: int) -> None:
    """
    Point Config at a build area without asking Minecraft for one.
    """
    Config().set_build_area_origin(x, z)
    Config().set_build_area_rect(x, z, x + x_length, z + z_length)


class FakeWorldSlice:
    """
    Stands in for http_utils.worldLoader.WorldSlice, which reads chunks from a running Minecraft instance.
    """

    def __init__(self, heightmap):
        self.heightmaps = {"MOTION_BLOCKING_NO_LEAVES": heightmap}
