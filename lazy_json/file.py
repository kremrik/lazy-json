import mmap
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

def get_next_char(
    mm: mmap.mmap,
    char: str
) -> int:
    cur_pos = tell(mm)
    char_pos = find(mm, char, cur_pos)
    seek(mm, char_pos + 1)
    return char_pos


def get_next_unescaped_char(
    mm: mmap.mmap,
    char: str
) -> int:
    cur_pos = tell(mm)
    char_pos = find(mm, char, cur_pos)
    seek(mm, char_pos + 1)

    prev = get(mm, char_pos - 1)  # will wrap around to -1
    if prev != "\\":
        return char_pos
    else:
        return get_next_unescaped_char(mm, char)


def get_next_non_whitespace_char(
    mm: mmap.mmap,
) -> int:
    whitespace = [" ", "\t", "\n"]
    cur_pos = tell(mm)
    seek(mm, cur_pos + 1)
    next_char = get(mm, cur_pos + 1)

    if next_char == "":
        return -1

    if next_char not in whitespace:
        return next_char
    else:
        return get_next_non_whitespace_char(mm)
