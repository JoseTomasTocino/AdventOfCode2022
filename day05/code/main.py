import logging
import re
from pprint import pprint as pp

logger = logging.getLogger(__name__)


def solution(inp, use_cratemover_9001=False):    
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

        # Part one
        if use_cratemover_9001 == False:
            for i in range(int(elem_count)):
                stacks[dest].append(stacks[source].pop())

        # Part two
        else:
            elems = [stacks[source].pop() for _ in range(int(elem_count))][::-1]
            stacks[dest] += elems
    
    return ''.join(x[-1] for x in stacks.values())


part_one = lambda x: solution(x, False)
part_two = lambda x: solution(x, True)
