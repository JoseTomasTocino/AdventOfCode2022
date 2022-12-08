from dataclasses import dataclass
import json
import logging
from functools import reduce  # forward compatibility for Python 3
from pprint import pprint, pformat
from enum import Enum
from collections import namedtuple

logger = logging.getLogger(__name__)


class FSElemType(Enum):
    DIR = 1
    FILE = 2


@dataclass
class FSElem:
    name: str
    type: FSElemType
    size: int
    children: dict


def compute_size(elem: FSElem):
    logger.info(f"Checking size of {elem.name}, type: {elem.type}")

    if elem.type == FSElemType.FILE:
        return elem.size
    else:
        return sum(compute_size(x) for x in elem.children.values())
    

def part_one(inp):
    fs = {'/': FSElem(name='/', type=FSElemType.DIR, size=0, children={})}
    cwd = ['/']
    all_directories = [fs['/']]

    inp = inp.splitlines()

    while inp:
        current = inp.pop(0)

        if current.startswith("$ cd "):
            dest_dir = current[5:]
            
            if dest_dir == '/':
                cwd = ['/']

            elif dest_dir == '..':
                cwd.pop()

            else:
                cwd.append(dest_dir)

            logger.info(f"Moved to directory {cwd[-1]}")
        
        elif current.startswith("$ ls"):
            logger.info(f"Listing the elements of directory {cwd[-1]}")

            # Traverse cwd hierarchy
            dir_node = fs
            for d in cwd:
                dir_node = dir_node[d].children

            while inp and not inp[0].startswith("$"):
                current = inp.pop(0)

                if current.startswith("dir"):
                    dirname = current[4:]
                    dir_node[dirname] = FSElem(name=dirname, type=FSElemType.DIR, size=0, children={})

                    # Keep a reference of all the directories in the fs
                    all_directories.append(dir_node[dirname])
                
                else:
                    fsize, fname = current.split(" ")
                    dir_node[fname] = FSElem(name=fname, type=FSElemType.FILE, size=int(fsize), children=None)


    # Now compute the sizes of the directories
    logger.info(all_directories)

    for d in all_directories:
        logger.info(f"Checking size of dir {d.name}, current size {d.size}")

        d.size = compute_size(d)
        logger.info(f"Calculated size: {d.size}")


    return sum(d.size for d in all_directories if d.size <= 100000)

def part_two(inp):
    pass
