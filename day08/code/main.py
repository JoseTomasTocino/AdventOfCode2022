import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    grid = []
    for row in inp.splitlines():
        grid.append([int(x) for x in row])

    visible_trees = len(grid[0]) * 2 + len(grid) * 2 - 4

    for j in range(1, len(grid) - 1):
        for i in range(1, len(grid[0]) - 1):
            current = grid[j][i]

            logger.info(f"Checking item @ ({i}, {j}) = {current}")

            # Left
            if all(x < current for x in grid[j][0:i]):
                visible_trees += 1
                continue

            # Right
            if all(x < current for x in grid[j][i+1:]):
                visible_trees += 1
                continue

            # Top
            if all(x < current for x in (grid[p][i] for p in range(0, j))):
                visible_trees += 1
                continue

            # Bottom
            if all(x < current for x in (grid[p][i] for p in range(j+1, len(grid[0])))):
                visible_trees += 1
                continue

    return visible_trees



def part_two(inp):
    pass
