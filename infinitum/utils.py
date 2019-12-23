#! /bin/python3
import logging

from typing import List


def read_list(path: str) -> List[str]:
    logging.debug(f"Reading csv list from path: '{path}'")
    content = None
    with open(path, 'r') as fp:
        content = fp.readlines()

    return [s.strip() for s in content]

    
