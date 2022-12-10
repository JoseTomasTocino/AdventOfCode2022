from enum import Enum
import logging

logger = logging.getLogger(__name__)


class State(Enum):
    INITIAL = 0
    DOING_NOOP = 1
    STARTING_ADDX = 2
    ENDING_ADDX = 3


def part_one(inp):
    register = 1
    cycle = 1
    state = State.INITIAL
    addx_operand = None

    strength_sum = 0

    opiter = iter(inp.splitlines())

    try:
        while True:

            # Start of cycle
            if state == State.INITIAL:
                op = next(opiter)

                if op.startswith("noop")    :
                    state = State.DOING_NOOP
                    pass

                elif op.startswith("addx"):
                    addx_operand = int(op[5:])
                    state = State.STARTING_ADDX

            elif state == State.DOING_NOOP:
                pass

            elif state == State.STARTING_ADDX:
                pass

            elif state == State.ENDING_ADDX:
                pass

            # Middle of cycle, check stuff
            if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
                strength_sum += cycle * register

            # End of cycle
            if state == State.STARTING_ADDX:
                state = State.ENDING_ADDX

            elif state == State.ENDING_ADDX:
                register += addx_operand
                state = State.INITIAL

            elif state == State.DOING_NOOP:
                state = State.INITIAL 

            cycle += 1

    except StopIteration:
        pass

    return strength_sum




def part_two(inp):
    pass
