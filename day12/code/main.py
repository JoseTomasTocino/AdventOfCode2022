from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain
import logging
from random import shuffle

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
    reverse_neighbors: list[Node] = field(default_factory=list)

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

        neighbors = [x for x in neighbors if self.height >= x.height - 1]

        for neighbor in neighbors:
            neighbor.reverse_neighbors.append(self)

        # logger.info(f"Neighbors of {self.position} are {[x.position for x in neighbors]}")

        self.neighbors = neighbors


def solution(inp, multiple_starting_points=False):
    matrix = inp.splitlines()
    node_map = defaultdict(dict)
    all_nodes = []

    logger.info(f"Map size is {len(matrix[0])}x{len(matrix)}")

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
    for node in all_nodes:
        node.compute_neighbors(node_map)

        logger.info(f"Node at {node.position} neighbors are: {[x.position for x in node.neighbors]}")

    path_lengths = []

    #####################################
    # REVERS'a'roooooo

    # Normal
    # start_node:Node = next(x for x in all_nodes if x.is_start)
    # end_node:Node = next(x for x in all_nodes if x.is_end)

    # Reversed
    start_node:Node = next(x for x in all_nodes if x.is_end)
    end_node:Node = next(x for x in all_nodes if x.is_start)

    for node in all_nodes:
        node.neighbors, node.reverse_neighbors = node.reverse_neighbors, node.neighbors
        logger.info(f"Node at {node.position} reverse neighbors are {[x.position for x in node.reverse_neighbors]}")
    

    #####################################

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
        for n in current.neighbors:
            if not n.visited:
                n.visited = True
                n.distance = 1 + current.distance
                n.pred = current

                queue.append(n)

                # if n.is_end:
                #     found = True
                #     break


    steps = 0

    if multiple_starting_points:
        pekers = [node for node in all_nodes if node.height == ord('a')]
    else:
        pekers = [end_node]

    shuffle(pekers)

    for node in pekers:
        nn = node
        # node:Node = end_node
        while node != start_node:
            node = node.pred        
            steps += 1

        logger.info(f"There are {steps} steps from end position at {nn.position} to start position at {start_node.position}")

        path_lengths.append(steps)

    return min(path_lengths)


part_one = lambda inp: solution(inp, multiple_starting_points=False)
part_two = lambda inp: solution(inp, multiple_starting_points=True)

