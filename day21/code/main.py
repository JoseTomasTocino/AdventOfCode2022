from dataclasses import dataclass
from enum import Enum
import logging
import operator
import re
from typing import Callable, Union

logger = logging.getLogger(__name__)


class MonkeyType(Enum):
    Number = 0
    Operation = 1


@dataclass
class Monkey:
    id: str
    typ: MonkeyType
    number: int = None
    operator_str: str = None
    operation: Callable = None
    left_operand: Union[str, "Monkey"] = None
    right_operand: Union[str, "Monkey"] = None
    stack: list = None


char_to_oper = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def solve_polish(inp, x=None):
    # if isinstance(stack[0], int):
    #     return stack[0]

    stack = []
    is_num = lambda x: isinstance(x, int) or isinstance(x, float)

    # logger.info(f"Solving {inp}")

    for i in inp:
        if i == 'x' and x is not None:
            i = x

        stack.append(i)
        # logger.info(f"Pushed {i}, current stack: {stack}")

        while len(stack) >= 3 and is_num(stack[-1]) and is_num(stack[-2]):
            op = char_to_oper[stack[-3]]
            res = op(stack[-2], stack[-1])

            # logger.info(f"Solving {stack[-2]} {stack[-3]} {stack[-1]}")

            stack.pop()
            stack.pop()
            stack.pop()

            stack.append(res)

    # logger.info(f"Final stack: {stack}")
    return stack[0]


def part_one(inp):
    """root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32"""

    monkeys:dict[Monkey] = {}

    # Create the monkeys
    for line in inp.splitlines():
        mid, mbody = line.split(": ")

        if any(x in mbody for x in "+-*/"):
            match = re.match(r"(.*?)\s+([\+\-\*\/])\s+(.*)", mbody)
            mleft, moper, mright = match.groups()
            moper_fun = char_to_oper[moper]

            monkeys[mid] = Monkey(id=mid, typ=MonkeyType.Operation, operator_str=moper, operation=moper_fun, left_operand=mleft, right_operand=mright)

        else:
            mnumber = int(mbody)
            monkeys[mid] = Monkey(id=mid, typ=MonkeyType.Number, number=mnumber)

    # Connect the monkeys
    for mid in monkeys:
        if monkeys[mid].typ == MonkeyType.Number:
            continue

        monkeys[mid].left_operand = monkeys[monkeys[mid].left_operand]
        monkeys[mid].right_operand = monkeys[monkeys[mid].right_operand]

    ######################################################################
    # Part one

    # Do a DFS to compute the values of the monkeys
    stack = [monkeys["root"]]
    monkeys_to_process = []

    while stack:
        monkey: Monkey = stack.pop(0)

        monkeys_to_process.insert(0, monkey)

        if monkey.typ == MonkeyType.Number:
            continue

        stack.insert(0, monkey.left_operand)
        stack.insert(0, monkey.right_operand)

    # Compute the "operation" monkeys in order
    monkey: Monkey
    for monkey in monkeys_to_process:

        if monkey.typ == MonkeyType.Number:
            if monkey.id == "humn":
                monkey.stack = ["x"]
            else:
                monkey.stack = [monkey.number]
        else:
            if monkey.id == "root":
                monkey.operator_str = "="

            monkey.number = monkey.operation(monkey.left_operand.number, monkey.right_operand.number)
            monkey.stack = [monkey.operator_str] + monkey.left_operand.stack + monkey.right_operand.stack

            if "x" not in monkey.stack:
                monkey.stack = [monkey.number]

    part_one_solution = monkeys["root"].number

    logger.info(monkeys["root"].stack)

    ######################################################################
    # Part two

    # Swap left and right branches if the X is in the right branch
    if 'x' in monkeys["root"].right_operand.stack:
        monkeys["root"].left_operand, monkeys["root"].right_operand = monkeys["root"].right_operand, monkeys["root"].left_operand
    
    left = monkeys["root"].left_operand.stack
    right = monkeys["root"].right_operand.stack

    rval = solve_polish(right)
    logger.info(f"{rval=}")

    # x = rval
    # last_x = None
    # while True:
    #     lval = solve_polish(left, x=x)
    #     logger.info(f"Trying with x={x}, lval={lval}")











    lvalt1 = solve_polish(left, x=rval)
    lvalt2 = solve_polish(left, x=-rval)

    comp = operator.lt

    if lvalt1 < lvalt2:
        logger.info(f"Function is decreasing")
        comp = operator.gt

    else:
        logger.info(f"Function is increasing")

    # logger.info(lvalt1)
    # logger.info(lvalt2)

    lval = None
    gone_past_over = False
    gone_past_under = False

    upper_bound = None
    lower_bound = None

    x = rval

    while True:
        logger.info("")

        lval = solve_polish(left, x=x)
        logger.info(f"Trying with x={x}, lval={lval}")

        if lval == rval:
            logger.info(f"BINGO!")
            break

        if comp(lval, rval):
            logger.info(f"X is too low")

            if lower_bound is None:
                lower_bound = x
            else:
                lower_bound = max(lower_bound, x)

            if lower_bound is not None and upper_bound is not None:
                x = (upper_bound - lower_bound) // 2 + lower_bound
            else:
                x *= 2

        else:
            logger.info(f"X is too high")

            if upper_bound is None:
                upper_bound = x
            else:
                upper_bound = min(upper_bound, x)

            if lower_bound is not None and upper_bound is not None:
                x = (upper_bound - lower_bound) // 2  + lower_bound

            else:
                x //= 2

        logger.info(f"Current interval [{lower_bound}, {upper_bound}]")

    return monkeys["root"].number, x
