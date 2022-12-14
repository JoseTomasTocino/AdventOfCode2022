import logging
import os.path
from ..code.main import part_one, solve_polish

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == (152, 301)
    # assert part_two(sample_input) == None


def test_polish_solver(caplog):
    caplog.set_level(logging.INFO)

    assert solve_polish(['+', '/', '+', 4, '*', 2, '-', 5, 3, 4, '*', '-', 32, 2, 5]) == 152


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == (157714751182692, 3373767893067)
        # assert part_two(content) == None
