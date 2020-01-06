#! /bin/python3
import logging

from typing import List


def read_list(path: str) -> List[str]:
    logging.debug(f"Reading csv list from path: '{path}'")
    content = None
    with open(path, 'r') as fp:
        content = fp.readlines()

    return [s.strip() for s in content]

def replace_html(html: str)->str:
    html = html.replace('\n', ' ').replace('\r', '')
    html = html.replace("&lt;", "<")
    html = html.replace("&gt;", ">")
    html = html.replace("&amp;", "&")
    return html
