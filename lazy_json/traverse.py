import mmap
from typing import Union


"""
File interaction abstraction wrapping `mmap`
"""


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
    end: int = -1
) -> int:
    if isinstance(char, str):
        char = char.encode()

    return mm.find(
        char,
        start,
        end
    )


def get(
    mm: mmap.mmap,
    index: int
) -> str:
    return mm[index:index+1].decode()


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
