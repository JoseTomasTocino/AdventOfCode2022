import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == (24, 93)


def test_big_input(caplog):
    caplog.set_level(logging.CRITICAL)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == (763, 23921)
        # assert part_two(content) == None
