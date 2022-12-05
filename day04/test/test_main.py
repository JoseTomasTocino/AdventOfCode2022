import logging
import os.path
from day04.code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)
    
    assert(part_one(sample_input) == 2)
    assert(part_two(sample_input) == None)


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert(part_one(content) == 644)
        # assert(part_two(content) == None)        
