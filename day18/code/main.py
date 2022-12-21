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
    air_cubes = []

    min_x, max_x = 9999, 0
    min_y, max_y = 9999, 0
    min_z, max_z = 9999, 0

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

    logger.info(f"{len(cubes)} cubes added")

    width = max_x - min_x + 1
    depth = max_y - min_y + 1
    height = max_z - min_z + 1
    area = width * depth * height

    logger.info(f"{min_x=}, {max_x=}")
    logger.info(f"{min_y=}, {max_y=}")
    logger.info(f"{min_z=}, {max_z=}")
    logger.info(f"{width} x {depth} x {height} = {area}")

    # Fill the cubemap with "air" cubes to fill in the voids
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_y, max_z + 1):
                if cubemap[x][y][z] is None:
                    the_air_cube = Cube(x, y, z, is_air=True)
                    cubemap[x][y][z] = the_air_cube
                    cubes.append(the_air_cube)

    logger.info(f"{len([x for x in cubes if x.is_air])} air cubes")

    # Now we need to search air clusters, starting at each "air cube" to see how much
    # that air cluster extends. We'll mark the air clusteras bad if we get out of bounds
    air_clusters = []

    for cube in cubes:
        if not cube.is_air or cube.visited:
            continue

        # Use a stack to keep track of adjacent air cubes, that will be visited in the loop below
        air_cluster_stack = [cube]
        air_cluster_components = set()

        # This flag marks whether the air cluster is bad (i.e. not enclosed by normal cubes)
        bad_air_cluster = False

        while air_cluster_stack:
            piece = air_cluster_stack.pop()
            piece.visited = True

            air_cluster_components.add((piece.x, piece.y, piece.z))

            # Check neighbours
            for dx, dy, dz in adjacencies:
                nx, ny, nz = piece.x + dx, piece.y + dy, piece.z + dz

                # Out of bounds air cluster? mark it as bad
                if nx < min_x or nx > max_x or ny < min_y or ny > max_y or nz < min_z or nz > max_z:
                    bad_air_cluster = True
                    

                neighbour = cubemap[nx][ny][nz]

                if neighbour is None or not neighbour.is_air or neighbour.visited:
                    continue

                air_cluster_stack.append(neighbour)

        if not bad_air_cluster:
            air_clusters.append(air_cluster_components)

    logger.info(f"Found {len(air_clusters)} possible air clusters")

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

    # Now compute the perimeter of the air clusters
    total_air_clusters_perimeters = 0

    for air_cluster in air_clusters:
        logger.info(f"Processing air cluster, components ({len(air_cluster)}): {air_cluster}")
        perimeter = 0

        air_cluster_neighbours = set()

        # if (11, 8, 18) in air_cluster:
        #     logger.info("SAY WAAAAAA")
        #     pdb.set_trace()

        for x, y, z in air_cluster:
            for dx, dy, dz in adjacencies:
                neighbour_coords = (x + dx, y + dy, z + dz)
                if neighbour_coords not in air_cluster:
                    air_cluster_neighbours.add(neighbour_coords)

        logger.info(f"{len(air_cluster_neighbours)} possible neighbours")

        for x, y, z in air_cluster_neighbours:
            neighbour = cubemap[x][y][z]
            if not neighbour.is_air:
                perimeter += 1
            else:
                pdb.set_trace()

        logger.info(f"The perimeter of this air cluster is {perimeter}")
        total_air_clusters_perimeters += perimeter

    return exposed_sides, exposed_sides - total_air_clusters_perimeters


def part_two(inp):
    pass
