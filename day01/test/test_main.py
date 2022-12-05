import logging
import os.path
from day01.code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 24000
    assert part_two(sample_input) == 45000


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        logger.info(f"Part one: {part_one(content)}")
        logger.info(f"Part two: {part_two(content)}")
