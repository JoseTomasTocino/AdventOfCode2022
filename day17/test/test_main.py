import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

def test_sample_input(caplog):
    caplog.set_level(logging.WARNING)

    assert part_one(sample_input) == 3068
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.WARNING)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 3232
        # assert part_two(content) == None
