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

    screen_width = 40
    screen_height = 6

    display = [[" "] * screen_width for _ in range(screen_height)]

    try:
        while True:

            # Start of cycle
            if state == State.INITIAL:
                op = next(opiter)

                if op.startswith("noop"):
                    state = State.DOING_NOOP
                    pass

                elif op.startswith("addx"):
                    addx_operand = int(op[5:])
                    state = State.STARTING_ADDX

                    logger.info(f"Start cycle   {cycle:3}: begin executing {op}")

            elif state == State.DOING_NOOP:
                pass

            elif state == State.STARTING_ADDX:
                pass

            elif state == State.ENDING_ADDX:
                logger.info(f"Start cycle   {cycle:3}: end executing {op}")
                pass

            # Middle of cycle, check stuff
            if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
                strength_sum += cycle * register

            current_pixel_x = (cycle - 1) % screen_width
            current_pixel_y = (cycle - 1) // screen_width

            logger.info(
                f"During cycle  {cycle:3}: CRT draws pixel in position {current_pixel_x}"
            )

            if current_pixel_x in (register - 1, register, register + 1):
                display[current_pixel_y][current_pixel_x] = "#"
            else:
                display[current_pixel_y][current_pixel_x] = "."

            logger.info(f"Current CRT row  : {''.join(display[current_pixel_y])}")

            # End of cycle
            if state == State.STARTING_ADDX:
                state = State.ENDING_ADDX

            elif state == State.ENDING_ADDX:
                register += addx_operand

                logger.info(
                    f"End of cycle  {cycle:3}: finish executing {op} (Register X is now {register})"
                )
                state = State.INITIAL

            elif state == State.DOING_NOOP:
                state = State.INITIAL

            cycle += 1
            logger.info("")

    except StopIteration:
        pass

    logger.info("\n" + "\n".join("".join(x) for x in display))

    return strength_sum


def part_two(inp):
    pass
