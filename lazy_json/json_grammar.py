from lazy_json import file
import json
import mmap
from typing import Callable, Generator


def parse_json(
    path: str
) -> Generator:
    mm = file.open_file(path)

    size = len(mm)
    pos = 0

    while pos < size and pos >= 0:
        print(pos, file.get(mm, pos))
        nxt = file.get_next_non_whitespace_char(mm, pos)

        if nxt.result in "{,":
            key, val = get_kv_bounds(mm, pos)
            pos = val.end + 1
            key_str = file.get(mm, key.bgn, key.end)
            val_str = file.get(mm, val.bgn, val.end)
            yield (key_str, val_str)
        elif nxt.result == "}":
            raise StopIteration


def get_kv_bounds(
    data,
    pos: int
) -> tuple:
    key = file.get_key_bound(data, pos + 1)
    val = file.get_value_bound(data, key.end)
    return key, val


if __name__ == "__main__":
    path = "/home/kemri/Projects/lazy-json/file_examples/simple.json"
    for i in parse_json(path):
        print(i)
