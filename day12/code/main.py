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
    distance: int = 0
    pred: Node = None


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
    all_nodes = []

    logger.info(f"Map size is {len(matrix[0])}x{len(matrix)}")

    start_position = None
    end_position = None

    # Generate Node instances from input matrix

    for y, row in enumerate(matrix):
        for x, elem in enumerate(row):

            is_start = False
            is_end = False

            if elem == "S":
                is_start = True
                elem = "a"

            elif elem == "E":
                is_end = True
                elem = "z"

            the_node = Node(
                height=ord(elem), position=Point(x, y), is_start=is_start, is_end=is_end
            )

            node_map[x][y] = the_node
            all_nodes.append(the_node)


    # Compute neighbors
    path_lengths = []

    start_node:Node = next(x for x in all_nodes if x.is_start)
    end_node:Node = next(x for x in all_nodes if x.is_end)

    start_node.visited = True
    start_node.distance = 0
    start_node.pred = None

    queue = [start_node]
    found = False

    logger.info(f"Starting at {start_node.position}")

    while queue and not found:
        current = queue.pop(0)

        logger.info(f"Visited {current.position}, height={current.height}")

        n:Node
        for n in current.get_neighbors(node_map=node_map):
            if not n.visited:
                n.visited = True
                n.distance = 1 + current.distance
                n.pred = current

                queue.append(n)

                if n.is_end:
                    found = True
                    break


    steps = 0

    node:Node = end_node
    while node != start_node:
        node = node.pred        
        steps += 1

    logger.info(f"There are {steps} steps from end position at {end_node.position} to start position at {start_node.position}")

    path_lengths.append(steps)

    return min(path_lengths)


part_one = lambda inp: solution(inp, multiple_starting_points=False)
part_two = lambda inp: solution(inp, multiple_starting_points=True)

