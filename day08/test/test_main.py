import logging
import os.path
from day08.code.main import solution, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """30373
25512
65332
33549
35390"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)
    
    visible_trees, scenic_score = solution(sample_input)

    assert visible_trees == 21
    assert scenic_score == 8


def test_big_input(caplog):
    caplog.set_level(logging.INFO)

    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        visible_trees, scenic_score = solution(content)

        assert visible_trees == 1717
        assert scenic_score == 321975
