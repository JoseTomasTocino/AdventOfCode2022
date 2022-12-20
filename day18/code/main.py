from __future__ import annotations

from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Cube:
    x: int
    y: int
    z: int

    def adjacent_to(self, other: Cube) -> bool:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) == 1


def part_one(inp):
    cubes = []
    for x, y, z in (x.split(',') for x in inp.splitlines()):
        cubes.append(Cube(int(x),int(y),int(z)))

    exposed_sides = len(cubes) * 6

    cube:Cube
    for cube in cubes:

        other_cube:Cube
        for other_cube in cubes:
            if cube.adjacent_to(other_cube):
                exposed_sides -= 1

    return exposed_sides


def part_two(inp):
    pass
