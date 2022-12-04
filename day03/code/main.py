import logging

logger = logging.getLogger(__name__)

def part_one(inp):
    acum = 0

    get_priority = lambda x: ord(x) - (96 if x.islower() else 38)

    for line in inp.splitlines():
        left, right = line[:len(line) // 2], line[len(line) // 2:]
        
        mismatched_item_type = (set(left) & set(right)).pop()

        acum += get_priority(mismatched_item_type)

    return acum

