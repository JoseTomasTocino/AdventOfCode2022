from functools import reduce
import logging

logger = logging.getLogger(__name__)

get_priority = lambda x: ord(x) - (96 if x.islower() else 38)


def part_one(inp):
    acum = 0

    for line in inp.splitlines():
        left, right = line[:len(line) // 2], line[len(line) // 2:]

        mismatched_item_type = (set(left) & set(right)).pop()

        acum += get_priority(mismatched_item_type)

    return acum


def part_two(inp):
    acum = 0

    group = []

    for line in inp.splitlines():
        group.append(line)

        if len(group) == 3:
            mismatched_item_type = reduce(lambda a, b: a & b, (set(x) for x in group)).pop()

            acum += get_priority(mismatched_item_type)

            group = []
    
    return acum
