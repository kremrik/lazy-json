from lazy_json.file import val_is_json_obj
from lazy_json import file
import json
from typing import Generator


def wrapper(
    path: str
) -> Generator:
    data = file.open_file(path)
    return parse(data, 0)


def parse(
    data,
    pos: int
) -> Generator:
    cont = True

    while cont:
        key = file.get_key(
            data,
            file.seek_to_key(data, pos)
        )

        val_pos = file.seek_to_val(data, key.end)

        if val_is_json_obj(data, val_pos):
            val = parse(data, val_pos)
        else:
            val = file.get_val(data, val_pos)

        pos = val.end  # ERROR: this will not work if val is result of recursive call

        yield key, val

        if file.end_of_json_obj(data, pos):
            cont = False
