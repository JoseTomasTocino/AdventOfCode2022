import logging

logger = logging.getLogger(__name__)


def solution(inp):
    grid = []
    for row in inp.splitlines():
        grid.append([int(x) for x in row])

    scenic_score = 0
    visible_trees = len(grid[0]) * 2 + len(grid) * 2 - 4

    for j in range(1, len(grid) - 1):
        for i in range(1, len(grid[0]) - 1):
            current = grid[j][i]

            logger.info(f"Checking item @ ({i}, {j}) = {current}")

            to_the_left = grid[j][0:i]
            to_the_right = grid[j][i + 1 :]
            to_the_top = [grid[p][i] for p in range(0, j)]
            to_the_bottom = [grid[p][i] for p in range(j + 1, len(grid[0]))]

            # Left
            if all(x < current for x in to_the_left):
                visible_trees += 1

            # Right
            elif all(x < current for x in to_the_right):
                visible_trees += 1

            # Top
            elif all(x < current for x in to_the_top):
                visible_trees += 1

            # Bottom
            elif all(x < current for x in to_the_bottom):
                visible_trees += 1

            # Second part
            to_the_left = to_the_left[::-1]
            to_the_top = to_the_top[::-1]

            views = [0, 0, 0, 0]

            for e in to_the_left:
                views[1] += 1
                if e >= current:
                    break

            for e in to_the_right:
                views[2] += 1
                if e >= current:
                    break

            for e in to_the_top:
                views[0] += 1
                if e >= current:
                    break

            for e in to_the_bottom:
                views[3] += 1
                if e >= current:
                    break

            logger.info(f"  Top:    {views[0]} {to_the_top}")
            logger.info(f"  Left:   {views[1]} {to_the_left}")
            logger.info(f"  Right:  {views[2]} {to_the_right}")
            logger.info(f"  Bottom: {views[3]} {to_the_bottom}")

            current_scenic_score = views[0] * views[1] * views[2] * views[3]

            logger.info(
                f"Item @ ({i}, {j}) = {current}, scenic score = {current_scenic_score}, {views=}"
            )

            scenic_score = max(scenic_score, current_scenic_score)
            logger.info("")

    return (visible_trees, scenic_score)


def part_two(inp):
    pass
