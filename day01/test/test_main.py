import logging
import os.path
from day01.code.main import main

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
    
    assert(main(sample_input) == 24000)


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        logger.info(main(content))
