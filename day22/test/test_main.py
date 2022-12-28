import logging
import os.path
from ..code.main import Direction, part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def test_directions(caplog):
    caplog.set_level(logging.INFO)


    d = Direction.Up
    assert Direction.turn_clockwise(d) == Direction.Right
    assert Direction.turn_counterclockwise(d) == Direction.Left


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 6032
    assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        # 149258 too high
        assert part_one(content) == None
        # assert part_two(content) == None
