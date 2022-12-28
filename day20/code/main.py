from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Node:
    value: int
    index: int
    prev: "Node" = None
    next: "Node" = None


    def get_next(self, steps):
        current = self

        while steps > 0:
            steps -= 1
            current = current.next

        return current


def print_nodes(n: Node) -> None:
    initial = n
    values = []

    while True:
        values.append(n.value)
        n = n.next
        if n == initial:
            break

    logger.info(", ".join(str(x) for x in values))


def part_one(inp):
    inp = [int(x) for x in inp.splitlines()]

    nodes = []

    for i, value in enumerate(inp):
        # Avoid unnecesary movements
        value = value % ((1 if value >= 0 else -1) * len(inp))

        n = Node(value=value, index=i, prev=None, next=None)
        nodes.append(n)

    # Connect nodes
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
        nodes[i + 1].prev = nodes[i]

    # Mix nodes
    original = nodes[:]
    logger.info("Initial arrangement:")
    print_nodes(nodes[0])

    for current in nodes:
        v = current.value
        if v == 0:
            logger.info(f"Ignoring {v=}")
            continue
                
        logger.info(f"Moving {v=}")
        aux = current
        while v != 0:
            if v < 0:
                aux = aux.prev
                v += 1

            elif v > 0:
                aux = aux.next
                v -= 1


        # Connect former prev and next together
        current.prev.next, current.next.prev = current.next, current.prev

        # Insert node in new place
        #  ###    <--->    ###
        # becomes:
        #  ### <-> ### <-> ###

        if current.value < 0:
            current.next = aux
            current.prev = aux.prev

            aux.prev = current
            current.prev.next = current

        else:
            current.prev = aux
            current.next = aux.next

            aux.next = current
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

    return v1.value + v2.value + v3.value

def part_two(inp):
    pass
