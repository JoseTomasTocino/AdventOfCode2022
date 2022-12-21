from __future__ import annotations
from collections import defaultdict

from dataclasses import dataclass
import json
import logging
import pdb

logger = logging.getLogger(__name__)


@dataclass
class Cube:
    x: int
    y: int
    z: int

    is_air: bool = False
    visited: bool = False

    def adjacent_to(self, other: Cube) -> bool:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) == 1


def part_one(inp):
    adjacencies = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

    cubemap = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
    cubes = []

    min_x, max_x = 9999, 0
    min_y, max_y = 9999, 0
    min_z, max_z = 9999, 0

    coords = []

    for x, y, z in (x.split(",") for x in inp.splitlines()):
        x, y, z = int(x), int(y), int(z)

        min_x = min(x, min_x)
        min_y = min(y, min_y)
        min_z = min(z, min_z)

        max_x = max(x, max_x)
        max_y = max(y, max_y)
        max_z = max(z, max_z)

        the_cube = Cube(x, y, z)
        cubes.append(the_cube)
        cubemap[x][y][z] = the_cube
        logger.debug(f"Added cube at {x}, {y}, {z}")

        coords.append((x,y,z))

    logger.debug(f"{len(cubes)} cubes added")
    logger.debug(coords)

    # Compute the exposed sides (as in part one)
    exposed_sides = 0

    cube: Cube
    for cube in cubes:
        if cube.is_air:
            continue

        x, y, z = cube.x, cube.y, cube.z

        for dx, dy, dz in adjacencies:
            neighbour = cubemap[x + dx][y + dy][z + dz]
            if neighbour is None or neighbour.is_air:
                exposed_sides += 1

    # For the second part, pick an empty location outside the bounds of the solid
    # cubes and do a BFS
    min_x -= 1
    min_y -= 1
    min_z -= 1
    max_x += 1
    max_y += 1
    max_z += 1

    width = max_x - min_x + 1
    depth = max_y - min_y + 1
    height = max_z - min_z + 1
    area = width * depth * height

    logger.debug(f"{min_x=}, {max_x=}")
    logger.debug(f"{min_y=}, {max_y=}")
    logger.debug(f"{min_z=}, {max_z=}")
    logger.debug(f"{width} x {depth} x {height} = {area}")

    out_of_bounds = lambda x,y,z: x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z

    really_exposed_sides = 0
    the_stack = [(min_x, min_y, min_z)]
    visited = set()

    while the_stack:
        x, y, z = the_stack.pop()

        if (x,y,z) in visited:  
            continue

        logger.debug(f"Checking {x}, {y}, {z}, {really_exposed_sides=}")
                
        visited.add((x,y,z))

        for dx, dy, dz in adjacencies:
            rx, ry, rz = x + dx, y + dy, z + dz

            if out_of_bounds(rx, ry, rz):
                logger.debug(f"  Neighbour at {rx}, {ry}, {rz} is out of bounds")
                continue

            elif (rx,ry,rz) in visited:
                logger.debug(f"  Neighbour at {rx}, {ry}, {rz} has been visited")
                continue

            elif cubemap[rx][ry][rz] is not None:
                logger.debug(f"  Neighbour at {rx}, {ry}, {rz} is a solid cube ####################################")
                really_exposed_sides += 1

            else:
                logger.debug(f"  Neighbour at {rx}, {ry}, {rz} added to coords to visit")
                the_stack.append((rx,ry,rz))

    return exposed_sides, really_exposed_sides


def part_two(inp):
    pass
