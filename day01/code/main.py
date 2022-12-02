import logging

logger = logging.getLogger(__name__)

def main(inp: str):
    max_so_far = 0
    current_elf_calories = 0

    for line in inp.splitlines():
        if not line:
            if current_elf_calories > max_so_far:
                max_so_far = current_elf_calories
            
            current_elf_calories = 0
        else:
            current_elf_calories += int(line.strip())

    return max(current_elf_calories, max_so_far) 

main = main