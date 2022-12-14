import logging

logger = logging.getLogger(__name__)


def matrix_str(matrix):
    height = len(matrix[0])

    lines = []
    for i in range(height):
        lines.append(f'{i:3} ' + ''.join([col[i] for col in matrix]))

    return '\n'.join(lines)


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

    # Matrix is stored as columns instead of as rows, so that matrix[0][2]
    # is the position x=0, y=2

    matrix = [['.'] * (grid_height + 2) for _ in range(grid_width + 3)]
    #matrix = [['.'] * (grid_width + 3) for _ in range(grid_height + 2)]
    
    logger.info(f"{grid_width=} {grid_height=}")
    logger.info('\n' + matrix_str(matrix))

    # Offset everything to the left
    for line in lines:
        line[0][0] -= leftmost - 1
        line[1][0] -= leftmost - 1

    # Place every line in the matrix
    for (start_x, start_y), (end_x, end_y) in lines:
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

    logger.info('\n' + matrix_str(matrix))

    # Start the pouring!
    units = 0
    overflowing = False

    while not overflowing:
        units += 1
        logger.info(f"Falling sand unit number {units}")
        
        unit_x = 500 - leftmost + 1
        unit_y = 0

        while True:
            if matrix[unit_x][unit_y + 1] == '.':
                unit_y += 1

            elif matrix[unit_x - 1][unit_y + 1] == '.':
                unit_x -= 1
                unit_y += 1

            elif matrix[unit_x + 1][unit_y + 1] == '.':
                unit_x += 1
                unit_y += 1

            else:
                matrix[unit_x][unit_y] = 'o'
                break

            if unit_y == bottommost:
                overflowing = True
                break
        
    logger.info('\n' + matrix_str(matrix))
    return units - 1
    

def part_two(inp):
    pass
