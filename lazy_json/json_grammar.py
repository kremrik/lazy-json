from lazy_json.file import get_value_bound
from lazy_json import file
import json
import mmap
from typing import Callable, Generator


def parse_json(
    data,
    pos: int
) -> Generator:
    pass


def parse_key_value_pair(
    data,
    pos: int
) -> tuple:
    """
    Call this function when you hit an opening brace

    `pos` is presumed to either precede the key, or begin the key.
    in either case, the beginning quote char of said key will be reflected.
    """
    key = file.get_key_bound(data, pos)

    pos = key.end  # different way of accessing position than find_sep.position
    find_sep = file.get_next_char(data, pos, ":")
    pos = find_sep.position

    determine_val = file.get_next_non_whitespace_char(data, pos)
    pos = determine_val.position

    if determine_val.result == "{":
        val = parse_json(data, pos + 1)  # won't work right now
    else:
        val = get_value_bound(data, pos)

    return key, val


if __name__ == "__main__":
    path = "/home/kemri/Projects/lazy-json/file_examples/simple.json"
    for i in parse_json(path):
        print(i)
