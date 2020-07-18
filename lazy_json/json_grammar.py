from lazy_json.file import val_is_json_obj
from lazy_json import file
import json
from typing import Generator


def get_kv(
    data,
    key: str
):
    correct_level = False
    pos = 0
    size = file.size(data)

    while not correct_level:
        found = file.get_next_char(data, pos, key)

        if pos >= size or found.position < 0:
            raise KeyError(f"Key '{key}' does not exist")
        
        # don't count first brace
        open_braces = file.count_between(data, "{", 0, found.position) - 1
        closed_braces = file.count_between(data, "{", 0, found.position)

        if open_braces > closed_braces:
            pos = found.position + 1
        else:
            correct_level = True
            
            key_bounds = file.get_key(data, pos - 1)  # -1 because we want quote
            val_pos = file.seek_to_val(data, key_bounds.end)

            if file.get(data, val_pos) == "{":
                val_bounds = file.get_val(data, val_pos)
            else:
                val_bounds = file.bound((val_pos, file.find_end_of_json(data, val_pos)))

    return key_bounds, val_bounds
