import logging

logger = logging.getLogger(__name__)


def solution(inp, window_size):

    for i in range(len(inp) - window_size):
        if len(set(inp[i : i + window_size])) == window_size:
            return i + window_size


part_one = lambda x: solution(x, 4)
part_two = lambda x: solution(x, 14)
