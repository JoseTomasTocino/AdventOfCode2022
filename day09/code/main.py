from copy import copy
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4


@dataclass
class Point:
    x: int
    y: int


def solution(inp, num_knots=2):
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

    knots = [Point(0, 0) for _ in range(num_knots)]

    visited_by_tail = set()

    for movement in movements:
        # for i in range(num_knots):
        #     logger.info(f"Knot {i} @ ({knots[i].x},{knots[i].y})")

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

        knots[0].x += delta_x
        knots[0].y += delta_y

        logger.info(f"Head moved to ({knots[0].x}, {knots[0].y})")

        for i in range(1, num_knots):
            current = knots[i]
            prev = knots[i - 1]

            # Compute new tail location
            distance_x = prev.x - current.x
            distance_y = prev.y - current.y

            if abs(distance_x) <= 1 and abs(distance_y) <= 1:
                # logger.info(f"Knot {i} did not move, {distance_x=}, {distance_y=}")
                pass

            else:
                if prev.x == current.x:
                    current.y += distance_y // 2
                    logger.info(
                        f"Moving knot {i} vertically   to {current.x}, {current.y}, {distance_x=}, {distance_y=}"
                    )

                elif prev.y == current.y:
                    current.x += distance_x // 2
                    logger.info(
                        f"Moving knot {i} horizontally to {current.x}, {current.y}, {distance_x=}, {distance_y=}"
                    )

                else:
                    if abs(distance_x) > abs(distance_y):
                        current.x += distance_x // 2
                        current.y = prev.y

                    elif abs(distance_x) < abs(distance_y):
                        current.x = prev.x
                        current.y += distance_y // 2

                    else:
                        current.x += distance_x // 2
                        current.y += distance_y // 2

                    logger.info(
                        f"Moving knot {i} diagonally   to {current.x}, {current.y}, {distance_x=}, {distance_y=}"
                    )

            if i == num_knots - 1:
                visited_by_tail.add((current.x, current.y))

        # matrix = [['.'] * 6 for x in range(5)]
        # letters = 'H123456789'

        # for i in reversed(range(num_knots)):
        #     matrix[4 - knots[i].y][knots[i].x] = letters[i]

        # logger.info('\n' + '\n'.join(''.join(x) for x in matrix))

    return len(visited_by_tail)


part_one = lambda x: solution(x, 2)
part_two = lambda x: solution(x, 10)
