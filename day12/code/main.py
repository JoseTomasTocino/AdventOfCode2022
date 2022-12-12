from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Node:
    height: str
    position: Point
    neighbors: list[Node] = field(default_factory=list)

    is_start: bool = False
    is_end: bool = False

    visited: bool = False

    def get_neighbors(self, node_map):

        map_height = len(next(iter(node_map.values())))
        map_width = len(node_map.values())

        neighbors = []

        if self.position.x > 0:
            neighbor:Node = node_map[self.position.x - 1][self.position.y]
            if neighbor.height <= self.height + 1:
                neighbors.append(neighbor)

        if self.position.y > 0:
            neighbor:Node = node_map[self.position.x][self.position.y - 1]
            if neighbor.height <= self.height + 1:
                neighbors.append(neighbor)

        if self.position.x < map_width - 1:
            neighbor:Node = node_map[self.position.x + 1][self.position.y]
            if neighbor.height <= self.height + 1:
                neighbors.append(neighbor)

        if self.position.y < map_height - 1:
            neighbor:Node = node_map[self.position.x][self.position.y + 1]
            if neighbor.height <= self.height + 1:
                neighbors.append(neighbor)

        return neighbors


def solution(inp, multiple_starting_points=False):
    matrix = inp.splitlines()
    node_map = defaultdict(dict)

    node_map_width = len(matrix[0])
    node_map_height = len(matrix)

    logger.info(f"Map size is {node_map_width}x{node_map_height}")

    start_position = None
    end_position = None

    for y, row in enumerate(matrix):
        for x, elem in enumerate(row):

            is_start = False
            is_end = False

            if elem == "S":
                is_start = True
                elem = "a"

                start_position = Point(x, y)

            elif elem == "E":
                is_end = True
                elem = "z"

                end_position = Point(x, y)

            node_map[x][y] = Node(
                height=ord(elem), position=Point(x, y), is_start=is_start, is_end=is_end
            )

    # Compute neighbors

    path_lengths = []
    starting_points = []

    if multiple_starting_points:
        logger.info(f"Finding starting points...")

        for i in node_map.values():
            for n in i.values():
                if n.height == ord('a'):
                    starting_points.append(n.position)
                    logger.info(f"    Starting at {n.position}")

    else:
        starting_points.append(start_position)


    for start_position in starting_points:

        logger.info(f"Starting at {start_position}")

        node: Node = node_map[start_position.x][start_position.y]
        node.visited = True

        queue = [node]
        distances = defaultdict(dict)
        pred = defaultdict(dict)

        distances[start_position.x][start_position.y] = 0

        found = False

        while queue and not found:
            current = queue.pop(0)

            logger.info(f"Visited {current.position}, height={current.height}")

            for n in current.get_neighbors(node_map=node_map):
                if not n.visited:
                    n.visited = True

                    distances[n.position.x][n.position.y] = 1 + distances[current.position.x][current.position.y]
                    pred[n.position.x][n.position.y] = current

                    queue.append(n)

                    if n.is_end:
                        found = True
                        break


        steps = 0
        pos = end_position

        while pos != start_position:
            pos = pred[pos.x][pos.y].position
            steps += 1

        logger.info(f"There are {steps} steps from end position at {end_position} to start position at {start_position}")

        path_lengths.append(steps)

    return min(path_lengths)


part_one = lambda inp: solution(inp, multiple_starting_points=False)
part_two = lambda inp: solution(inp, multiple_starting_points=True)

