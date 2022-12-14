from itertools import zip_longest
import logging
import re
from enum import Enum

logger = logging.getLogger(__name__)


class Outcome(Enum):
    RIGHT_ORDER = 1
    CONTINUE_COMPARING = 2
    WRONG_ORDER = 3


def compare(left, right, indent = 0):
    

    if left is None:
        logger.info(f"{'  ' * indent}- Compare {left} vs {right}")
        return Outcome.RIGHT_ORDER

    elif right is None:
        logger.info(f"{'  ' * indent}- Compare {left} vs {right}")
        return Outcome.WRONG_ORDER

    elif isinstance(left, int) and isinstance(right, int):
        logger.info(f"{'  ' * indent}- Compare {left} vs {right} - int vs int")

        if left < right:
            return Outcome.RIGHT_ORDER

        elif left > right:
            return Outcome.WRONG_ORDER

        elif left == right:
            return Outcome.CONTINUE_COMPARING

    elif isinstance(left, list) and isinstance(right, list):
        logger.info(f"{'  ' * indent}- Compare {left} vs {right} - list vs list")

        for subleft, subright in zip_longest(left, right, fillvalue=None):
            logger.info(f"{'  ' * indent}- {subleft=} {subright=}")

            outcome = compare(subleft, subright, indent + 1)

            if outcome == Outcome.CONTINUE_COMPARING:
                continue

            else:
                return outcome

        return Outcome.CONTINUE_COMPARING

    elif isinstance(left, list) and isinstance(right, int):
        logger.info(f"{'  ' * indent}- Compare {left} vs {right} - list vs int")
        return compare(left, [right], indent + 1)

    elif isinstance(left, int) and isinstance(right, list):
        logger.info(f"{'  ' * indent}- Compare {left} vs {right} - int vs list")
        return compare([left], right, indent + 1)

    else:
        raise ValueError


def part_one(inp):
    correct_pair_indices = []

    for i, pair_raw in enumerate(re.split(r"\n\n", inp)):
        logger.info(f"== Pair {i + 1} ==")
        left, right = [eval(x) for x in pair_raw.split("\n")]
        outcome = compare(left, right)

        if outcome == Outcome.RIGHT_ORDER:
            logger.info("Right order")
            correct_pair_indices.append(i+1)
        elif outcome == Outcome.WRONG_ORDER:
            logger.info("Wrong order")
        else:
            logger.info("WTF")

        logger.info("")

    return sum(correct_pair_indices)


def part_two(inp):
    pass
