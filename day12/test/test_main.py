import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""



def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 31
    # assert part_two(sample_input) == 29


def test_big_input(caplog):
    caplog.set_level(logging.CRITICAL)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 481
        # assert part_two(content) == None
