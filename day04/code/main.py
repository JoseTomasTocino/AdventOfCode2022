import logging
import re

logger = logging.getLogger(__name__)


def solution(inp, partial_overlap=False):
    acum = 0
    exp = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

    for line in inp.splitlines():
        a0, a1, b0, b1 = (int(x) for x in exp.match(line).groups())

        logger.info(f"A: [{a0}-{a1}], B: [{b0}-{b1}]")

        if not partial_overlap:
            if (a0 <= b0 and a1 >= b1) or (b0 <= a0 and b1 >= a1):
                logger.info("Contained!")
                acum += 1
        else:
            if a0 > b0:
                a0, a1, b0, b1 = b0, b1, a0, a1

            if a1 >= b0:
                logger.info("Overlap!")
                acum +=1


    return acum


part_one = lambda inp: solution(inp, False)
part_two = lambda inp: solution(inp, True)
