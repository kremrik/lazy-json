from lazy_json import file
from functools import partial
from typing import Generator


"""
Can we separate these into layers again?
"""


class ljson(object):
    def __init__(self, data, start: int, end: int):
        self.data = data
        self.start = start
        self.end = end

    def __getitem__(self, key: str):
        # walker = walk_json(self.data, self.start, self.end)
        for k, v in walk_json(self.data, self.start, self.end):
            keyname = file.get_json_from_bound(self.data, k)

            if keyname == key:
                if isinstance(v, ljson):
                    return v
                else:
                    val = file.get_json_from_bound(self.data, v)
                    return val
        else:
            raise KeyError(key)

    def keys(self):
        # walker = walk_json(self.data, self.start, self.end)
        for k, _ in walk_json(self.data, self.start, self.end):
            keyname = file.get_json_from_bound(self.data, k)
            yield keyname

    def values(self):
        # walker = walk_json(self.data, self.start, self.end)
        for _, v in walk_json(self.data, self.start, self.end):
            if isinstance(v, ljson):
                yield v
            else:
                value = file.get_json_from_bound(self.data, v)
                yield value

    def items(self):
        # walker = walk_json(self.data, self.start, self.end)
        for k, v in walk_json(self.data, self.start, self.end):
            key = file.get_json_from_bound(self.data, k)
            if isinstance(v, ljson):
                val = v
            else:
                val = file.get_json_from_bound(self.data, v)
            yield key, val


def walk_json(
    data,
    start: int,
    end: int
) -> Generator:
    pos = start

    while 1:
        # TODO: abstraction breach
        if file.get_next_non_whitespace_char(data, pos).position == end:
            break

        key = file.get_key(
            data,
            file.seek_to_key(data, pos)
        )

        val_pos = file.seek_to_val(data, key.end)

        if file.val_is_json_obj(data, val_pos):
            inner_start = val_pos
            inner_end = pos = file.find_end_of_json(data, val_pos)
            val = ljson(data, inner_start, inner_end)
        else:
            val = file.get_val(data, val_pos)
            pos = val.end

        yield key, val


def load(
    fp
):
    fileno = fp.name
    mm = partial(file.load_mm, path=fileno)
    size = file.end_of_file(mm)
    return ljson(mm, 0, size)
