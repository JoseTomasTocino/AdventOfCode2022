from dataclasses import dataclass
from functools import reduce
import operator
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class Monkey:
    number: int
    items: list

    operation_type: str
    operation_left_operand: str
    operation_right_operand: str

    divisibility_test: int
    target_if_true: int
    target_if_false: int

    num_inspections: int = 0

    def do_operation(self, n):
        if self.operation_left_operand == "old":
            left = n
        else:
            left = int(self.operation_left_operand)

        if self.operation_right_operand == "old":
            right = n
        else:
            right = int(self.operation_right_operand)

        if self.operation_type == "+":
            return left + right

        elif self.operation_type == "*":
            return left * right

        else:
            raise NotImplementedError

    def do_test(self, n):
        return n % self.divisibility_test == 0


def solution(inp, divide_worry_levels=True):
    monkeys: list[Monkey] = []

    inp = inp.splitlines()
    oper_re = re.compile(r"^new = (.*) ([\*\+]) (.*)$")

    while True:
        if not inp:
            break

        current = inp.pop(0)

        if current.startswith("Monkey "):
            monkey = int(current[len("Monkey ") : -1])
            logger.info(f"Parsing monkey {monkey}")

            # Next line: Starting items: a, b, c
            current = inp.pop(0)
            monkey_items = [
                int(x.strip()) for x in current[current.index(":") + 1 :].split(", ")
            ]
            logger.info(f"Starting items: {monkey_items}")

            # Next line: Operation
            current = inp.pop(0)
            monkey_operation_raw = current[current.index(": ") + 2 :]
            logger.info(f"Operation: '{monkey_operation_raw}'")

            match = oper_re.match(monkey_operation_raw)
            monkey_operation_operand_left = match.group(1)
            monkey_operation_operator = match.group(2)
            monkey_operation_operand_right = match.group(3)

            logger.info(match.groups())

            logger.info(
                f"Operator: {monkey_operation_operator}, left: {monkey_operation_operand_left}, right: {monkey_operation_operand_right}"
            )

            # Next line: test
            current = inp.pop(0)
            monkey_divisibility_test = int(current[current.index("by ") + 3 :])
            logger.info(f"Monkey test: '{monkey_divisibility_test}'")

            # Next line: actions
            current = inp.pop(0)
            monkey_target_if_true = int(current[current.index("y") + 2 :])
            logger.info(f"If true: throw to monkey {monkey_target_if_true}")

            current = inp.pop(0)
            monkey_target_if_false = int(current[current.index("y") + 2 :])
            logger.info(f"If false: throw to monkey {monkey_target_if_false}")

            m = Monkey(
                number=monkey,
                items=monkey_items,
                operation_type=monkey_operation_operator,
                operation_left_operand=monkey_operation_operand_left,
                operation_right_operand=monkey_operation_operand_right,
                divisibility_test=monkey_divisibility_test,
                target_if_true=monkey_target_if_true,
                target_if_false=monkey_target_if_false,
            )

            monkeys.append(m)

            logger.info("")

    # In part two, the "worry levels" are not divided by three, so we need a different
    # way of reducing those numbers so they don't get too big. The way of reducing the
    # items values without affecting the behaviour is by making sure the divisibility tests
    # keep the same results. In order to achieve that we can just divide the item values
    # by a common multiple of all the divisors of the monkeys. There's no need to use the
    # least common multiple tho, so just multiplying them will do.
    reductor = reduce(operator.mul, (x.divisibility_test for x in monkeys), 1)

    round = 1
    max_rounds = 20 if divide_worry_levels else 10000

    while round <= max_rounds:
        logger.info(f"Round: {round}")

        for monkey in monkeys:
            logger.info(f"Monkey {monkey.number}: ")

            while monkey.items:
                item = monkey.items.pop(0)
                monkey.num_inspections += 1

                logger.info(f"  Monkey inspects an item with a worry level of {item}")

                item = monkey.do_operation(item)
                logger.info(f"    Worry level changes to {item}")

                if divide_worry_levels:
                    item = item // 3
                    logger.info(f"    Worry level is divided by 3 to {item}")

                else:
                    item = item % reductor
                    logger.info(f"    Worry level moduloed by {reductor}")

                if monkey.do_test(item):
                    logger.info(
                        f"    Test passed, item is thrown to {monkey.target_if_true}"
                    )
                    monkeys[monkey.target_if_true].items.append(item)

                else:
                    logger.info(
                        f"    Test failed, item is thrown to {monkey.target_if_false}"
                    )
                    monkeys[monkey.target_if_false].items.append(item)

        logger.info("")
        logger.info(
            f"After round {round}, the monkeys are holding items with these worry levels:"
        )

        for monkey in monkeys:
            logger.info(
                f"Monkey {monkey.number}: {','.join(str(x) for x in monkey.items)}"
            )

        round += 1

    for monkey in monkeys:
        logger.info(
            f"Monkey {monkey.number} inspected items {monkey.num_inspections} times."
        )

    inspections = list(sorted([m.num_inspections for m in monkeys], reverse=True))

    return inspections[0] * inspections[1]


part_one = lambda x: solution(x, True)
part_two = lambda x: solution(x, False)
