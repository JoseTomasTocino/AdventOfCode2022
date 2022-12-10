from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4


def part_one(inp):
    movements = []

    for line in inp.splitlines():
        direction, steps = line.split(" ")

        if direction == "R":
            direction = Direction.RIGHT
        elif direction == "L":
            direction = Direction.LEFT
        elif direction == "U":
            direction = Direction.UP
        elif direction == "D":
            direction = Direction.DOWN
        else:
            raise ValueError

        for i in range(int(steps)):
            movements.append(direction)

    head_x, head_y = (0, 0)
    tail_x, tail_y = (0, 0)

    visited_by_tail = set()

    for movement in movements:
        delta_y = 0
        delta_x = 0

        if movement == Direction.UP:
            delta_y = 1

        elif movement == Direction.DOWN:
            delta_y = -1

        elif movement == Direction.LEFT:
            delta_x = -1

        elif movement == Direction.RIGHT:
            delta_x = 1

        previous_x, previous_y = head_x, head_y

        head_x += delta_x
        head_y += delta_y

        # Compute new tail location
        dist_x = head_x - tail_x
        dist_y = head_y - tail_y

        logger.info(f"Head moved to ({head_x}, {head_y})")

        if abs(dist_x) <= 1 and abs(dist_y) <= 1:
            logger.info("Tail did not move")
            pass

        else:
            if head_x == tail_x:
                tail_y += dist_y // 2

            elif head_y == tail_y:
                tail_x += dist_x // 2

            else:
                tail_x, tail_y = previous_x, previous_y

            logger.info(f"Tail moved to ({tail_x}, {tail_y})")

        visited_by_tail.add((tail_x, tail_y))

        logger.info("")

        # matrix = [['.'] * 6 for x in range(5)]
        # matrix[4 - head_y][head_x] = 'H'
        # matrix[4 - tail_y][tail_x] = 'T'

        # logger.info('\n' + '\n'.join(''.join(x) for x in matrix))

    return len(visited_by_tail)


def part_two(inp):
    pass
