import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    topmost = 0
    bottommost = -1
    leftmost = 9999999
    rightmost = -1


    lines = []
    for line in inp.splitlines():
        line_vertices = line.split(' -> ')
        line_vertices = [x.split(',') for x in line_vertices]
        line_vertices = [[int(y) for y in x] for x in line_vertices]

        logger.info(line_vertices)

        # Find leftmost and rightmost points
        leftmost = min(leftmost, *[x[0] for x in line_vertices])
        rightmost = max(rightmost, *[x[0] for x in line_vertices])

        topmost = min(topmost, *[x[1] for x in line_vertices])
        bottommost = max(bottommost, *[x[1] for x in line_vertices])

        for i, vertex_a in enumerate(line_vertices[:-1]):
            lines.append((vertex_a, line_vertices[i+1][:]))
    
    logger.info(f"{leftmost=}, {rightmost=}")
    logger.info(f"{topmost=}, {bottommost=}")

    grid_width = rightmost - leftmost
    grid_height = bottommost - topmost

    
    matrix = [['.'] * (grid_width + 3) for _ in range(grid_height + 2)]
    
    logger.info(f"{grid_width=} {grid_height=}")
    logger.info('\n' + '\n'.join([''.join(x) for x in matrix]))

    # Offset everything left to (1, 0)

    for line in lines:
        logger.info(line)
        line[0][0] -= leftmost - 1
        line[1][0] -= leftmost - 1
        logger.info(line)


    for (start_x, start_y), (end_x, end_y) in lines:
        logger.info(f"{start_x=} {start_y=} {end_x=} {end_y=}")

        # Vertical
        if start_x == end_x:
            if start_y > end_y:
                start_y, end_y = end_y, start_y

            for y in range(start_y, end_y + 1):
                matrix[y][start_x] = "#"

        else:
            if start_x > end_x:
                start_x, end_x = end_x, start_x

            for x in range(start_x, end_x + 1):
                matrix[start_y][x] = "#"

    logger.info('\n' + '\n'.join([''.join(x) for x in matrix]))

            


def part_two(inp):
    pass
