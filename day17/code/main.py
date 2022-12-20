from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import itertools
import json
import logging
import pdb

from day17.code.visualization import Viz

logger = logging.getLogger(__name__)

CAVE_WIDTH = 7


class RockType(Enum):
    Horizontal = 1
    Cross = 2
    Angle = 3
    Vertical = 4
    Square = 5


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rock:
    type: RockType
    elems: list = None

    def move_by(self, x: int, y: int):
        for e in self.elems:
            e.x += x
            e.y += y

    def top_shape(self):
        """Returns a list of tuples (x, h) where x is the horizontal coordinate, and
        h is the height of the rock at that x position"""

        x_coords = list(sorted(set(e.x for e in self.elems)))
        return [(x, max(e.y for e in self.elems if e.x == x)) for x in x_coords]

    def top(self):
        return max(p.y for p in self.elems)

    def collides_with(self, collision_grid):
        for e in self.elems:
            if collision_grid[e.x][e.y]:
                return True

        if any(e.x < 0 for e in self.elems):
            return True
        
        if any(e.x >= CAVE_WIDTH for e in self.elems):
            return True
        
        return False


    @classmethod
    def build_from_type(cls, rock_type):
        the_rock = cls(type=rock_type, elems=cls.get_template(rock_type))
        return the_rock

    @staticmethod
    def get_template(rock_type: RockType):
        if rock_type == RockType.Horizontal:
            return deepcopy([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)])

        elif rock_type == RockType.Cross:
            return deepcopy([Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 0), Point(1, 2)])

        elif rock_type == RockType.Angle:
            return deepcopy([Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)])

        elif rock_type == RockType.Vertical:
            return deepcopy([Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)])

        elif rock_type == RockType.Square:
            return deepcopy([Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)])


def pp_cg(fun, grid, temp_rock=None):
    highest_point = 0
    # X is a defualtdict with with pairs like {y: bool}
    for x in grid.values():
        for y, v in x.items():
            if v and y > highest_point:
                highest_point = y
        

    # highest_point = max(sum([list(x.keys()) for x in grid.values()], start=[]))
    fun(f"{highest_point=}")

    if temp_rock:
        highest_point = max(highest_point, max(p.y for p in temp_rock.elems))

    for y in range(highest_point, -1, -1):
        rc = ['.'] * CAVE_WIDTH
        for x in range(CAVE_WIDTH):
            if grid[x][y]:
                rc[x] = '#' if y != 0 else '-'

            if temp_rock and (x,y) in [(p.x, p.y) for p in temp_rock.elems]:
                rc[x] = '@'

        if y == 0:
            fun(f"{y:5} +{''.join(rc)}+")
        else:
            fun(f"{y:5} |{''.join(rc)}|")

        if y < highest_point - 40:
            break

DO_VIZ = False
DRAW_START = False
DRAW_INTERMEDIATE = False
DRAW_END = True
DRAW_FINAL = True


def part_one(inp):
    peaks = [0] * CAVE_WIDTH

    rock_number = 0
    rock_type_list = [RockType.Horizontal, RockType.Cross, RockType.Angle, RockType.Vertical, RockType.Square]
    rock_type_iter = itertools.cycle(rock_type_list)

    movement_iter = itertools.cycle(enumerate(inp.strip()))

    all_rocks = []
    collision_grid = defaultdict(lambda: defaultdict(lambda: False))
    for i in range(7):
        collision_grid[i][0] = True

    memo = {}

    if DO_VIZ:
        v = Viz()

    while rock_number < 2022:
        rock_number += 1
        current_rock_type = next(rock_type_iter)

        logger.info("")
        logger.warning(f"NEW ROCK: Rock number {rock_number} is a {current_rock_type:20}, current max height: {max(peaks)}")
        rock:Rock = Rock.build_from_type(current_rock_type)
        all_rocks.append(rock)
        logger.info(rock.elems)

        logger.debug(f"Moving rock two units away from the left wall")
        rock.move_by(x=2, y=0)
        logger.debug(rock.elems)

        logger.debug(f"Placing rock three units on top of highest rock or floor")
        rock.move_by(x=0, y=max(peaks) + 4)
        logger.debug(rock.elems)

        logger.debug("")
        logger.debug("Starting movement loop:")

        if DRAW_START:
            pp_cg(logging.warning, collision_grid, rock)

        for mov_i, movement in movement_iter:

            # peak_delta = tuple([peaks[0] - x for x in peaks])
            # logger.warning(peak_delta)

            # if (peak_delta, current_rock_type, mov_i) in memo:
            #     cycle_rock_number, cycle_height = memo[(peak_delta, current_rock_type, mov_i)]

            #     logger.warning(f"Found cycle between rock number {cycle_rock_number}, h={cycle_height} and {rock_number}, h={max(peaks)}")

            #     cycle_duration = cycle_rock_number - rock_number
                
            #     return 0

            # memo[(peak_delta, current_rock_type, mov_i)] = (rock_number, max(peaks))

            # Lateral movement
            temp_rock = deepcopy(rock)

            if movement == '<':
                temp_rock.move_by(x=-1, y=0)
                # logger.info("Jet of gas pushes to the left")
            else:
                temp_rock.move_by(x=1, y=0)
                # logger.info("Jet of gas pushes to the right")

            if temp_rock.collides_with(collision_grid):
                logger.info(f"Movement {movement} had no effect")
            else:
                # Apply movement to actual rock
                logger.info(f"Movement {movement} applied")
                rock.elems = temp_rock.elems

            if DRAW_INTERMEDIATE:
                pp_cg(logging.info, collision_grid, rock)

            if DO_VIZ:
                v.draw(collision_grid, rock)
            
            # Falling
            logger.info("Rock falls one unit")
            temp_rock = deepcopy(rock)
            temp_rock.move_by(x=0, y=-1)
            logger.debug(f"temp rock: {temp_rock.elems}")

            if temp_rock.collides_with(collision_grid):
                logger.info(f"Rock stops")
                break
            else:
                # Apply movement to actual rock
                rock.elems = temp_rock.elems
            
            if DRAW_INTERMEDIATE:
                pp_cg(logging.info, collision_grid, rock)

            if DO_VIZ:
                v.draw(collision_grid, rock)

            logger.debug(f"{rock.elems}")
            logger.debug("")

        # Mark positions of the resting rock as occupied in collision grid
        for e in rock.elems:
            collision_grid[e.x][e.y] = True

        # # Remove elements in collision grid that are 50 units away from current rock
        # for x in list(collision_grid.keys()):
        #     for y in list(collision_grid[x].keys()):
        #         if y < e.y - 40:
        #             collision_grid[x].pop(y)

        # Update peaks
        for x, h in rock.top_shape():
            peaks[x] = max(peaks[x], h)

        # v.draw(collision_grid)
        if DRAW_END:
            pp_cg(logging.warning, collision_grid)
        
    # pdb.set_trace()
    if DRAW_FINAL:
        pp_cg(logging.warning, collision_grid)

    if DO_VIZ:
        v.draw(collision_grid)
        v.run()

    return max(peaks)


def part_two(inp):
    pass
