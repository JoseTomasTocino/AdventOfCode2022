from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain
import logging
from random import shuffle
from .dijkstra import Graph

logger = logging.getLogger(__name__)


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Node:
    number: int
    height: int
    position: Point
    neighbors: list[Node] = field(default_factory=list)

    is_start: bool = False
    is_end: bool = False

    visited: bool = False
    distance: int = 0
    pred: Node = None

    def compute_neighbors(self, node_map):

        map_height = len(next(iter(node_map.values())))
        map_width = len(node_map.values())

        neighbors = []

        if self.position.x > 0:
            neighbors.append(node_map[self.position.x - 1][self.position.y])

        if self.position.y > 0:
            neighbors.append(node_map[self.position.x][self.position.y - 1])

        if self.position.x < map_width - 1:
            neighbors.append(node_map[self.position.x + 1][self.position.y])

        if self.position.y < map_height - 1:
            neighbors.append(node_map[self.position.x][self.position.y + 1])

        neighbors = [
            neighbor for neighbor in neighbors if neighbor.height <= self.height + 1
        ]

        self.neighbors = neighbors

    def __str__(self) -> str:
        return f"[{self.number}, {chr(self.height)} @ ({self.position.x}, {self.position.y}){' S ' if self.is_start else ''}{' E ' if self.is_end else ''}]"


def solution(inp, multiple_starting_points=False):
    matrix = inp.splitlines()
    node_map = defaultdict(dict)
    all_nodes = []

    map_width = len(matrix[0])
    map_height = len(matrix)

    logger.info(f"Map size is {map_width}x{map_height}")

    g = Graph(map_width * map_height)

    start_node = None
    end_node = None

    # Generate Node instances from input matrix
    for y, row in enumerate(matrix):
        for x, elem in enumerate(row):
            node_number = y * map_width + x

            is_start = False
            is_end = False

            if elem == "S":
                is_start = True
                elem = "a"
                start_node = node_number

            elif elem == "E":
                is_end = True
                elem = "z"
                end_node = node_number

            the_node = Node(
                number=node_number,
                height=ord(elem),
                position=Point(x, y),
                is_start=is_start,
                is_end=is_end,
            )

            node_map[x][y] = the_node
            all_nodes.append(the_node)

            logger.info(f"Processed node {the_node}")

    logger.info(f"Start node is node number {start_node}")
    logger.info(f"End node is node number {end_node}")

    # Compute neighbors
    node: Node
    for node in all_nodes:
        node.compute_neighbors(node_map)

        neighbor: Node
        for neighbor in node.neighbors:
            # Edge is inverted because we need to walk backwards from end to start
            # g.add_edge(node.number, neighbor.number, 1)
            logger.info(f"Added edge between {neighbor} and {node}")
            g.add_edge(neighbor.number, node.number, 1)

        logger.info(
            f"Node {node} neighbors are: {', '.join(str(x) for x in node.neighbors)}"
        )

    d = g.dijkstra(end_node)

    if multiple_starting_points:
        return min(d[x.number] for x in all_nodes if x.height == ord("a"))
    else:
        return d[start_node]


part_one = lambda inp: solution(inp, multiple_starting_points=False)
part_two = lambda inp: solution(inp, multiple_starting_points=True)
