from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Node:
    value: int
    movement: int
    index: int
    prev: "Node" = None
    next: "Node" = None


    def get_next(self, steps):
        current = self

        while steps > 0:
            steps -= 1
            current = current.next

        return current


    def get_previous(self, steps):
        current = self

        while steps > 0:
            steps -= 1
            current = current.prev

        return current


    def __str__(self) -> str:
        # return f"Node with value={self.value:6}, movement = {self.movement}, prev node = {self.prev.value}, next node = {self.next.value}"
        return f"Node with value={self.value:6}, prev node = {self.prev.value:6}, next node = {self.next.value:6}"


def print_nodes(n: Node) -> None:
    initial = n
    values = []

    while True:
        values.append(n.value)
        n = n.next
        if n == initial:
            break

    logger.info(", ".join(str(x) for x in values))


def solution(inp, multiplier=1, mixing_times=1):
    inp = [int(x) for x in inp.splitlines()]

    nodes = []

    for i, value in enumerate(inp):
        value *= multiplier

        # Avoid unnecesary movements
        movement = value % (len(inp) - 1)

        n = Node(value=value, movement=movement, index=i, prev=None, next=None)
        nodes.append(n)

    logger.info(f"Number of nodes {len(nodes)}, unique numbers: {len(set(inp))}")

    # Connect nodes
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
        nodes[i + 1].prev = nodes[i]

    # Mix nodes
    for _ in range(mixing_times):
        for current in nodes:
            v = current.movement
            if v == 0:
                logger.info(f"Ignoring {current.value=} {current.movement=}")
                # print_nodes(nodes[0])
                continue
                    
            logger.info(f"Moving {current.value=}, {current.movement=}")
            if v > 0:
                aux = current.get_next(v)
            else:
                aux = current.get_previous(abs(v))

            assert current.prev.next == current
            assert current.next.prev == current

            # Connect former neighbours together
            current.prev.next, current.next.prev = current.next, current.prev

            # Insert node in new place
            #  ###    <--->    ###
            # becomes:
            #  ### <-> CUR <-> ###

            if current.movement < 0:
                current.prev = aux.prev
                current.next = aux

                aux.prev = current

            else:
                current.prev = aux
                current.next = aux.next

                aux.next = current

            current.prev.next = current
            current.next.prev = current

    print_nodes(nodes[0])

    # Find the node with value 0
    node: Node
    for node in nodes:
        if node.value == 0:
            break

    v1 = node.get_next(1000 % len(inp))
    v2 = node.get_next(2000 % len(inp))
    v3 = node.get_next(3000 % len(inp))

    logger.info(f"Number at position 1000 is: {v1.value}")
    logger.info(f"Number at position 2000 is: {v2.value}")
    logger.info(f"Number at position 3000 is: {v3.value}")

    return v1.value + v2.value + v3.value


part_one = lambda x: solution(x, 1, 1)
part_two = lambda x: solution(x, 811589153, 10)

