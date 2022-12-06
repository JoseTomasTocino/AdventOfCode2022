import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    window_size = 4

    logger.info(f"Input: {inp}")

    for i in range(len(inp) - window_size):
        logger.info(f"Checking {inp[i:i+window_size]}")

        if len(set(inp[i:i+window_size])) == window_size:
            return i + window_size



def part_two(inp):
    pass
