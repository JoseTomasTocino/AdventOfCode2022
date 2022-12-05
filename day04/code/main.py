import logging
import re

logger = logging.getLogger(__name__)


def part_one(inp):
    acum = 0
    exp = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

    for line in inp.splitlines():
        a0, a1, b0, b1 = (int(x) for x in exp.match(line).groups())

        logger.info(f"A: [{a0}-{a1}], B: [{b0}-{b1}]")

        if (a0 <= b0 and a1 >= b1) or (b0 <= a0 and b1 >= a1):
            logger.info("Contained!")
            acum += 1

    return acum
        


def part_two(inp):
    pass