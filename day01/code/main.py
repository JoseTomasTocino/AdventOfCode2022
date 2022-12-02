import logging
import heapq

logger = logging.getLogger(__name__)

def main(inp: str, n: int):
    """
    Use a heap to keep the n highest calories counts
    """
    calories_per_elf = []
    current_elf_calories = 0
    
    # Add an additional empty element to trigger the base case at the end of the list
    for line in inp.splitlines() + [""]:
        if not line:
            heapq.heappush(calories_per_elf, current_elf_calories)
            current_elf_calories = 0
        else:
            current_elf_calories += int(line.strip())

    return sum(heapq.nlargest(n, calories_per_elf))


part_one = lambda x: main(x, 1)
part_two = lambda x: main(x, 3)