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
    operation: Callable = None
    left_operand: Union[str, "Monkey"] = None
    right_operand: Union[str, "Monkey"] = None


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

    monkeys = {}

    # Create the monkeys
    for line in inp.splitlines():
        mid, mbody = line.split(": ")

        if any(x in mbody for x in "+-*/"):
            match = re.match(r"(.*?)\s+([\+\-\*\/])\s+(.*)", mbody)
            mleft, moper, mright = match.groups()
            moper = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}[moper]

            monkeys[mid] = Monkey(id=mid, typ=MonkeyType.Operation, operation=moper, left_operand=mleft, right_operand=mright)

        else:
            mnumber = int(mbody)
            monkeys[mid] = Monkey(id=mid, typ=MonkeyType.Number, number=mnumber)

    # Connect the monkeys
    for mid in monkeys:
        if monkeys[mid].typ == MonkeyType.Number:
            continue
            
        monkeys[mid].left_operand = monkeys[monkeys[mid].left_operand]
        monkeys[mid].right_operand = monkeys[monkeys[mid].right_operand]

    # Do a DFS to compute the values of the monkeys
    stack = [monkeys["root"]]
    monkeys_to_process = []

    while stack:
        current:Monkey = stack.pop(0)

        if current.typ == MonkeyType.Number:
            continue

        monkeys_to_process.insert(0, current)
        stack.insert(0, current.left_operand)
        stack.insert(0, current.right_operand)
        
    # Compute the "operation" monkeys in order
    monkey: Monkey
    for monkey in monkeys_to_process:
        monkey.number = monkey.operation(monkey.left_operand.number, monkey.right_operand.number)

    return monkeys["root"].number



    


def part_two(inp):
    pass
