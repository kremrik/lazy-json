from lazy_json.file import val_is_json_obj
from lazy_json import file
import json
from typing import Generator


class ljson(object):
    def __init__(self, data, start: int, end: int):
        self.data = data
        self.start = start
        self.end = end

    def __getitem__(self, key: str):
        walker = walk_json(self.data, self.start, self.end)
        for kv in walker:
            k = kv[0]
            v = kv[1]

            # TODO: using lower-level abstraction than it should
            keyname = file.get(
                mm=self.data,
                start=k.bgn,
                end=k.end
            ).replace('"', "")

            if keyname == key:
                if isinstance(v, ljson):
                    return v
                else:
                    # TODO: using lower-level abstraction than it should
                    _val = file.get(
                        mm=self.data,
                        start=v.bgn,
                        end=v.end
                    )
                    return json.loads(_val)
        else:
            raise KeyError(key)


def walk_json(
    data,
    start: int,
    end: int
) -> Generator:
    pos = start

    while 1:
        if pos >= end:
            break

        if file.get_next_non_whitespace_char(data, pos).position == end:
            break

        # TODO: need another check here to call schemes abstraction to determine
        #  if we're at the end of the file, irrespective of whitespace

        key = file.get_key(
            data,
            file.seek_to_key(data, pos)
        )

        val_pos = file.seek_to_val(data, key.end)

        if val_is_json_obj(data, val_pos):
            inner_start = val_pos
            inner_end = pos = file.find_end_of_json(data, val_pos)
            val = ljson(data, inner_start, inner_end)
        else:
            val = file.get_val(data, val_pos)
            pos = val.end

        yield key, val


def starter(
    path: str
) -> ljson:
    data = file.open_file(path)
    size = file.end_of_file(data)
    return ljson(data, 0, size)
