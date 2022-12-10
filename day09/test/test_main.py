import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 13
    assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 5902
        # assert(part_two(content) == None)
