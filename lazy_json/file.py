import mmap
from collections import namedtuple
from os import name
from typing import Union


"""
File interaction abstraction wrapping `mmap`
"""


# mmap traversal primitives
#------------------------------------------------------------------------------


def open_file(
    path: str,
) -> mmap.mmap:
    with open(path, "r") as j:
        mm = mmap.mmap(
            j.fileno(), 
            0,  # not sure if this is wise
            access=mmap.ACCESS_READ
            )
    return mm


def find(
    mm: mmap.mmap,
    char: Union[bytes, str],
    start: int = 0,
    end: int = None
) -> int:
    if isinstance(char, str):
        char = char.encode()

    if not end:
        return mm.find(
            char,
            start
        )
    else:
        return mm.find(
            char,
            start,
            end
        )


def get(
    mm: mmap.mmap,
    start: int,
    end: int = None
) -> str:
    if not end:
        end = start + 1
    return mm[start:end].decode()


def tell(
    mm: mmap.mmap
) -> int:
    return mm.tell()


def seek(
    mm: mmap.mmap,
    pos: int
) -> None:
    # side-effect-y
    return mm.seek(pos)


# mmap traversal combinations
#------------------------------------------------------------------------------
mmap_result = namedtuple("mmap_result", ["result", "position"])


def get_next_char(
    mm: mmap.mmap,
    pos: int,
    char: str
) -> mmap_result:
    char_pos = find(mm, char, pos)
    return mmap_result(char_pos, char_pos)


def get_next_unescaped_char(
    mm: mmap.mmap,
    pos: int,
    char: str
) -> mmap_result:
    char_pos = find(mm, char, pos)
    pos += 1

    prev = get(mm, char_pos - 1)  # will wrap around to -1
    if prev != "\\":
        return mmap_result(char_pos, char_pos)
    else:
        return get_next_unescaped_char(mm, pos, char)


def get_next_non_whitespace_char(
    mm: mmap.mmap,
    pos: int
) -> mmap_result:
    whitespace = [" ", "\t", "\n"]

    next_char = get(mm, pos)

    if next_char == "":
        return mmap_result(None, pos)

    if next_char not in whitespace:
        return mmap_result(next_char, pos)
    else:
        return get_next_non_whitespace_char(mm, pos + 1)


def get_prev_non_whitespace_char(
    mm: mmap.mmap,
    pos: int
) -> mmap_result:
    whitespace = [" ", "\t", "\n"]
    pos -= 1

    prev_char = get(mm, pos)

    if prev_char == "":
        return mmap_result(None, pos)

    if prev_char not in whitespace:
        return mmap_result(prev_char, pos)
    else:
        return get_prev_non_whitespace_char(mm, pos)


# mmap traversal schemes
#------------------------------------------------------------------------------
bound = namedtuple("bound", ["bgn", "end"])


def get_key_bound(
    mm: mmap.mmap,
    pos: int
) -> bound:
    key_bgn = get_next_char(mm, pos, '"')
    key_end = get_next_unescaped_char(mm, key_bgn.position + 1, '"')
    return bound(key_bgn.position + 1, key_end.position)


def get_value_bound(
    mm: mmap.mmap,
    pos: int
) -> bound:
    colon = get_next_char(mm, pos, ":")
    bgn = get_next_non_whitespace_char(mm, colon.position + 1)
    
    if bgn.result != '"':
        bgn_val = bgn.position
        comma = get_next_char(mm, bgn.position + 1, ",")
        brace = get_next_char(mm, bgn.position + 1, "}")

        if comma.result == -1 or (brace.position < comma.position):
            end_val = get_prev_non_whitespace_char(mm, brace.position).position + 1
        else:
            end_val = comma.position

    else:
        bgn_val = bgn.position + 1
        end_val = get_next_unescaped_char(mm, bgn.position + 1, '"').position

    return bound(bgn_val, end_val)
