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

def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 64
    assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 3542
        # assert part_two(content) == None
