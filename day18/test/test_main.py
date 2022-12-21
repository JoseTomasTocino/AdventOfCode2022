import logging
import os.path
from ..code.main import Cube, part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def test_adjacency(caplog):
    caplog.set_level(logging.INFO)

    c1 = Cube(1,1,1)
    c2 = Cube(2,1,1)
    c3 = Cube(3,1,1)

    assert c1.adjacent_to(c2)
    assert c2.adjacent_to(c3)
    assert not c1.adjacent_to(c3)

def test_equality(caplog):
    c1 = Cube(1,1,1)
    c2 = Cube(1,1,1)

    assert c1 == c2

def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    # assert part_one(sample_input) == (64, 58)

    # 1 x 1 x 1
    inp = """1,1,1"""

    assert part_one(inp) == (6, 6)


    # 2 x 2 x 2, no air gaps
    inp = """1,1,1
2,1,1
1,2,1
2,2,1
1,1,2
2,1,2
1,2,2
2,2,2"""

    assert part_one(inp) == (24, 24)

        # 3 cubes, L shape
    inp = """1,1,1
2,1,1
1,1,2"""

    assert part_one(inp) == (14, 14)

    # 8 cubes, O shape (hole in the middle)
    inp = """1,1,1
2,1,1
3,1,1
1,1,2
3,1,2
1,1,3
2,1,3
3,1,3"""

    assert part_one(inp) == (32, 32)

    # 3 x 3 x 3 cube, hollow in the middle
    inp = """1,1,1
2,1,1
3,1,1
1,1,2
2,1,2
3,1,2
1,1,3
2,1,3
3,1,3
1,2,1
2,2,1
3,2,1
1,2,2
3,2,2
1,2,3
2,2,3
3,2,3
1,3,1
2,3,1
3,3,1
1,3,2
2,3,2
3,3,2
1,3,3
2,3,3
3,3,3"""

    assert part_one(inp) == (60, 54)
    

        # 3 x 4 x 3 cube, hollow in the middle (missing 2,2,2 and 2,3,2)
    inp = """1,1,1
2,1,1
3,1,1
1,1,2
2,1,2
3,1,2
1,1,3
2,1,3
3,1,3
1,2,1
2,2,1
3,2,1
1,2,2
3,2,2
1,2,3
2,2,3
3,2,3
1,3,1
2,3,1
3,3,1
1,3,2
3,3,2
1,3,3
2,3,3
3,3,3
1,4,1
2,4,1
3,4,1
1,4,2
2,4,2
3,4,2
1,4,3
2,4,3
3,4,3"""

    outer = 9 * 2 + 12 * 4
    inner = 10
    assert part_one(inp) == (outer + inner, outer)


        # 3 x 3 x 3 cube, hollow from the center upwards
    inp = """1,1,1
2,1,1
3,1,1
1,1,2
2,1,2
3,1,2
1,1,3
2,1,3
3,1,3
1,2,1
2,2,1
3,2,1
1,2,2
3,2,2
1,2,3
3,2,3
1,3,1
2,3,1
3,3,1
1,3,2
2,3,2
3,3,2
1,3,3
2,3,3
3,3,3"""

    assert part_one(inp) == (62, 62)

    # 5 x 5 x 5 cube, hollow inside (1 cube thick walls)

    s = []
    zz = []
    for x in range(1, 6):
        for y in range (1, 6):
            for z in range(1, 6):
                s.append(','.join((str(x),str(y),str(z))))
                zz.append((x,y,z))

    for x in range(2, 5):
        for y in range (2, 5):
            for z in range(2, 5):
                s.remove(','.join((str(x),str(y),str(z))))
                zz.remove((x,y,z))
    
    logging.info(zz)

    ss = '\n'.join(s)
    assert part_one(ss) == (25*6 + 9 * 6, 25*6)

    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        # 1184 for part two is TOO LOW
        # 2058 is invalid
        # 2697 is too high
        assert part_one(content) == (3542, 2080)
        # assert part_two(content) == None
