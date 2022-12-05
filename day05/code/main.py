import logging
import re
from pprint import pprint as pp

logger = logging.getLogger(__name__)


def part_one(inp):    
    stack_lines = []
    movement_lines = []

    reading_movements = False

    # Read stack definition until an empty line appears, then read movements
    for line in inp.splitlines():
        if not line:
            reading_movements = True
            continue

        if not reading_movements:
            stack_lines.append(line)
        else:
            movement_lines.append(line)
    
    stack_numbers = stack_lines.pop().split()

    stacks = {x: [] for x in stack_numbers}

    # Create a regular expression to parse stack lines depending on the number of stacks
    stack_line_re = re.compile(' '.join(['.(.).'] * len(stacks)))

    for line in stack_lines[::-1]:
        logger.info(line)

        for i, elem in enumerate(stack_line_re.match(line).groups()):
            if elem.strip():
                stacks[str(i+1)].append(elem)

    movement_re = re.compile(r'move (\d+) from (\d+) to (\d+)')
    for movement in movement_lines:
        elem_count, source, dest = movement_re.match(movement.strip()).groups()

        for i in range(int(elem_count)):
            stacks[dest].append(stacks[source].pop())
    
    return ''.join(x[-1] for x in stacks.values())

def part_two(inp):
    pass
