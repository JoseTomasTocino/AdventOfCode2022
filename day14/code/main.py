from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


def matrix_str(matrix):
    min_x, max_x = min(matrix.keys()), max(matrix.keys())
    min_y, max_y = 0, max(max(x) for x in matrix.values())

    width = max_x + 1
    height = max_y + 1

    logger.info(f"{min_x=}, {max_x=}")
    logger.info(f"{min_y=}, {max_y=}")
    logger.info(f"{width=}, {height=}")

    graph = [["."] * width for _ in range(height)]

    for x, subm in matrix.items():
        for y, n in subm.items():
            graph[y][x] = n

    lines = []
    for i, row in enumerate(graph):
        lines.append(f"{i:3} " + "".join("".join(row)))

    return "\n".join(lines)


def part_one(inp):
    topmost = 0
    bottommost = -1
    leftmost = 9999999
    rightmost = -1

    lines = []
    for line in inp.splitlines():
        line_vertices = line.split(" -> ")
        line_vertices = [x.split(",") for x in line_vertices]
        line_vertices = [[int(y) for y in x] for x in line_vertices]

        logger.info(line_vertices)

        # Find leftmost and rightmost points
        leftmost = min(leftmost, *[x[0] for x in line_vertices])
        rightmost = max(rightmost, *[x[0] for x in line_vertices])

        topmost = min(topmost, *[x[1] for x in line_vertices])
        bottommost = max(bottommost, *[x[1] for x in line_vertices])

        for i, vertex_a in enumerate(line_vertices[:-1]):
            lines.append((vertex_a, line_vertices[i + 1][:]))

    logger.info(f"{leftmost=}, {rightmost=}")
    logger.info(f"{topmost=}, {bottommost=}")

    # Matrix is a map of nodes (dict of dicts)
    matrix = defaultdict(lambda: defaultdict(lambda: "."))

    floor = bottommost + 2
    logger.info(f"Floor is at y={floor}")

    # Offset everything to the left
    for line in lines:
        line[0][0] -= leftmost - 1
        line[1][0] -= leftmost - 1

    # Place every line in the matrix
    for (start_x, start_y), (end_x, end_y) in lines:
        logger.info(f"Placing line from {start_x},{start_y} to {end_x},{end_y}")

        # Vertical
        if start_x == end_x:
            if start_y > end_y:
                start_y, end_y = end_y, start_y

            for y in range(start_y, end_y + 1):
                matrix[start_x][y] = "#"

        else:
            if start_x > end_x:
                start_x, end_x = end_x, start_x

            for x in range(start_x, end_x + 1):
                matrix[x][start_y] = "#"

    logger.info("\n" + matrix_str(matrix))

    # Start the pouring!
    units = 0
    units_until_overflow = None
    reached_top = False

    while not reached_top:
        units += 1

        unit_x = 500 - leftmost + 1
        unit_y = 0

        while True:
            if unit_y == floor - 1:
                matrix[unit_x][unit_y] = "o"
                break

            if matrix[unit_x][unit_y + 1] == ".":
                unit_y += 1

            elif matrix[unit_x - 1][unit_y + 1] == ".":
                unit_x -= 1
                unit_y += 1

            elif matrix[unit_x + 1][unit_y + 1] == ".":
                unit_x += 1
                unit_y += 1

            else:
                matrix[unit_x][unit_y] = "o"

                if unit_y == 0:
                    reached_top = True

                break

            if unit_y == bottommost and units_until_overflow is None:
                units_until_overflow = units - 1

    return units_until_overflow, units


def part_two(inp):
    pass
