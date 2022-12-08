import logging
import os.path
from day07.code.main import solution

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    sol_p1, sol_p2 = solution(sample_input)
    assert sol_p1 == 95437
    assert sol_p2 == 24933642


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        sol_p1, sol_p2 = solution(content)
        assert sol_p1 == 1454188
        assert sol_p2 == 4183246
