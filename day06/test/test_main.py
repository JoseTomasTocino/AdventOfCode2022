import logging
import os.path
from day06.code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = None


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert part_one("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part_one("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part_one("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part_one("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert(part_one(content) == 1287)
        # assert(part_two(content) == None)
