from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, IntEnum
import logging
import re

logger = logging.getLogger(__name__)


class Direction(IntEnum):
    Up = 3
    Left = 2
    Down = 1
    Right = 0

    @staticmethod
    def turn_clockwise(d):
        return Direction((int(d) + 1) % 4)

    @staticmethod
    def turn_counterclockwise(d):
        return Direction((int(d) - 1) % 4)

    @staticmethod
    def delta(d):
        return {Direction.Up: (0, -1), Direction.Left: (-1, 0), Direction.Down: (0, 1), Direction.Right: (1, 0)}[d]


@dataclass
class Tile:
    x: int
    y: int
    is_wall: bool = False

    top: "Tile" = None
    left: "Tile" = None
    right: "Tile" = None
    bottom: "Tile" = None

    def neighbor(self, d: Direction):
        if d == Direction.Up:
            return self.top

        if d == Direction.Left:
            return self.left

        if d == Direction.Down:
            return self.bottom

        if d == Direction.Right:
            return self.right


def part_one(inp):
    map: defaultdict[defaultdict[Tile]] = defaultdict(lambda: defaultdict(lambda: None))
    all_tiles = []

    path = None
    h_bounds = {}  # key is row number
    v_bounds = {}  # key is col number

    for y, row in enumerate(inp.splitlines()):
        if not row:
            break

        for x, item in enumerate(row):
            if item == " ":
                continue

            if y not in h_bounds:
                h_bounds[y] = (x, x)

            else:
                hb0, hb1 = h_bounds[y]
                h_bounds[y] = (min(x, hb0), max(x, hb1))

            if x not in v_bounds:
                v_bounds[x] = (y, y)

            else:
                vb0, vb1 = v_bounds[x]
                v_bounds[x] = (min(y, vb0), max(y, vb1))

            if item == ".":
                t = Tile(x, y)
                map[x][y] = t
                all_tiles.append(t)

            elif item == "#":
                t = Tile(x, y, is_wall=True)
                map[x][y] = t
                all_tiles.append(t)

    # # Connect neighbors
    for tile in all_tiles:
        x, y = tile.x, tile.y

        hb0, hb1 = h_bounds[y]
        vb0, vb1 = v_bounds[x]

        # HORIZONTAL NEIGHBOURS

        # Tile's on the left edge and right edge is not a wall
        if x == hb0 and not map[hb1][y].is_wall:
            tile.left = map[hb1][y]

        elif map[x - 1][y] is not None and not map[x - 1][y].is_wall:
            tile.left = map[x - 1][y]

        # Tile's on the right edge and left edge is not a wall
        if x == hb1 and not map[hb0][y].is_wall:
            tile.right = map[hb0][y]

        elif map[x + 1][y] is not None and not map[x + 1][y].is_wall:
            tile.right = map[x + 1][y]

        # VERTICAL NEIGHBOURS

        # Tile's on the top edge and bottom edge is not a wall
        if tile.y == vb0 and not map[x][vb1].is_wall:
            tile.top = map[x][vb1]

        elif map[x][tile.y - 1] is not None and not map[x][tile.y - 1].is_wall:
            tile.top = map[x][tile.y - 1]

        # Tile's on the bottom edge and top edge is not a wall
        if tile.y == vb1 and not map[x][vb0].is_wall:
            tile.bottom = map[x][vb0]

        elif map[x][tile.y + 1] is not None and not map[x][tile.y + 1].is_wall:
            tile.bottom = map[x][tile.y + 1]

    # MOVEMENT
    y = 0
    x = h_bounds[y][0]

    current_direction = Direction.Right
    current_tile: Tile = map[x][y]

    logger.info(f"Starting at {x},{y}")

    path = inp.splitlines()[-1]

    for steps, turn_to in re.findall(r"(\d+?)([RL])", path):
        logger.info(f"Movement, {steps} steps, direction: {str(current_direction)}")

        for _ in range(int(steps)):
            neighbor = current_tile.neighbor(current_direction)

            if neighbor is not None:
                current_tile = neighbor
                logger.info(f"Moved to {current_tile.x},{current_tile.y}")

        if turn_to == "L":
            current_direction = Direction.turn_counterclockwise(current_direction)

        else:
            current_direction = Direction.turn_clockwise(current_direction)

    return 1000 * (current_tile.y + 1) + 4 * (current_tile.x + 1) + current_direction


def part_two(inp):
    pass
