import json
import mmap
from collections import namedtuple
from typing import Union


"""
File interaction abstraction wrapping `mmap`
"""


#------------------------------------------------------------------------------
# TODO: stateful function
def load_mm(
    path: str,
    reset: int = 1000000
):
    """
    NOTE:   `reset` is the number of calls that have been made to `load_mm`
            after which a new mmap will be created. We can probably make it
            dynamic relative to the system's hardware.

    Due to the weird issue of mmap traversals eating up memory without bound,
    we have two options:
      1. chunk the mmap using `length` and `offset`
      2. reload the mmap every once in a while

    Option 1 makes it very difficult to materialize json elements because a
    given key/value might span multiple chunks, and we'd have to create a new
    mmap object first for finding the bounds, then for retrieving the json.

    Option 2 is not the least bit sexy, but it's by far the simpler of the two. 
    And it succeeds in making this a CPU-bound problem instead of memory or IO.

    Option 2 requires the use of some state to determine the following:
      - How many calls have been made using the same mmap (under a certain
        threshold should reuse the same mmap)
      - What was the last mmap created (if we're under said threshold, return 
        the same mmap seen last time)
      - Is this the same file we've already mapped (if we get a new file path,
        start the process over again)
    """
    if load_mm.calls % reset == 0 or path != load_mm.file:
        with open(path, "r") as j:
            mm = mmap.mmap(
                j.fileno(),
                0,
                access=mmap.ACCESS_READ
            )
        load_mm.file = path
        load_mm.mm = mm
        load_mm.calls = 0

    load_mm.calls += 1
    return load_mm.mm

load_mm.file = None
load_mm.mm = None
load_mm.calls = 0


def find(
    mm,
    char: Union[bytes, str],
    start: int = 0,
    end: int = None,
    side: str = "left"
) -> int:
    mm = mm()

    sides = {
        "left": mm.find,
        "right": mm.rfind
    }
    _find = sides[side]

    if isinstance(char, str):
        char = char.encode()

    if not end:
        return _find(
            char,
            start
        )
    else:
        return _find(
            char,
            start,
            end
        )


def get(
    mm,
    start: int,
    end: int = None
) -> str:
    """non-inclusive end"""
    _mm = mm()
    if not end:
        end = start + 1
    return _mm[start:end].decode()


def size(
    mm
) -> int:
    mm = mm()
    return mm.size()


#------------------------------------------------------------------------------
mmap_result = namedtuple("mmap_result", ["result", "position"])


def get_next_char(
    mm,
    pos: int,
    char: str
) -> mmap_result:
    """
    will find the next value INCLUSIVE to current position
    """
    char_pos = find(mm, char, pos)
    return mmap_result(char_pos, char_pos)


def get_next_unescaped_char(
    mm,
    pos: int,
    char: str
) -> mmap_result:
    while 1:
        char_pos = find(mm, char, pos)
        prev = get(mm, char_pos - 1)
        if prev != "\\":
            return mmap_result(char_pos, char_pos)
        else:
            pos += 1


def get_next_non_whitespace_char(
    mm,
    pos: int
) -> mmap_result:
    whitespace = [" ", "\t", "\n"]
    while 1:
        next_char = get(mm, pos)
        if next_char == "":
            return mmap_result(None, pos)
        if next_char not in whitespace:
            return mmap_result(next_char, pos)
        else:
            pos += 1


def get_prev_non_whitespace_char(
    mm,
    pos: int
) -> mmap_result:
    whitespace = [" ", "\t", "\n"]
    while 1:
        pos -= 1
        prev_char = get(mm, pos)

        if prev_char == "":
            return mmap_result(None, pos)
        if prev_char not in whitespace:
            return mmap_result(prev_char, pos)
        else:
            pass


#------------------------------------------------------------------------------
bound = namedtuple("bound", ["bgn", "end"])


def count_between(
    mm,
    sub: str,
    start: int,
    end: int
) -> int:
    """
    count is inclusive to `start` and `end`
    """
    count = 0
    pos = start
    
    while 1:
        found = get_next_char(mm, pos, sub)
        if found.position == -1 or found.position > end:
            break
        count += 1
        pos = found.position + 1

    return count


def find_end_of_json(
    mm,
    pos: int
) -> int:
    """
    `pos` must be the opening brace of a JSON object
    """
    opens = 0
    closeds = 0

    opens += 1  # include the opening brace

    while opens > closeds:
        o = get_next_char(mm, pos + 1, "{")
        c = get_next_char(mm, pos + 1, "}")

        if o.position > 0 and (o.position < c.position):
            opens += 1
            pos = o.position
        else:
            closeds += 1
            pos = c.position

    return pos


def end_of_json_obj(
    mm,
    pos: int
) -> bool:
    """
    Reaches out past the current position to see if the current position is
    actually the last character before the end of the JSON block
    """
    nxt = get_next_non_whitespace_char(mm, pos)
    if nxt.result == "}":
        return True
    return False


def end_of_file(
    mm,
) -> int:
    # TODO: breaks abstraction bounds, may need to refactor `get_next`
    return find(mm, "}", -1, None, "right")


def val_is_json_obj(
    mm,
    pos: int
) -> bool:
    if get(mm, pos) == "{":
        return True
    return False


def seek_to_key(
    mm,
    pos: int
) -> int:
    return get_next_char(mm, pos, '"').position


def seek_to_val(
    mm: mmap.mmap,
    pos: int
) -> int:
    colon = get_next_char(mm, pos, ":")
    return get_next_non_whitespace_char(mm, colon.position + 1).position


def get_key(
    mm,
    pos: int
) -> bound:
    """
    given the `pos` indicating the beginning of a key, return the end position
    """
    key_end = get_next_unescaped_char(mm, pos + 1, '"')
    return bound(pos, key_end.position + 1)


def get_val(
    mm,
    pos: int
) -> bound:
    """
    given the `pos` indicating the beginning of a value, return the end position
    """
    bgn = get_next_non_whitespace_char(mm, pos)
    
    if bgn.result != '"':
        bgn_val = bgn.position
        comma = get_next_char(mm, bgn.position + 1, ",")
        brace = get_next_char(mm, bgn.position + 1, "}")

        if comma.result == -1 or (brace.position < comma.position):
            end_val = get_prev_non_whitespace_char(mm, brace.position).position + 1
        else:
            end_val = comma.position

    else:
        bgn_val = bgn.position
        end_val = get_next_unescaped_char(mm, bgn.position + 1, '"').position + 1

    return bound(bgn_val, end_val)


def get_json_from_bound(
    mm,
    b: bound
):
    bgn = b.bgn
    end = b.end
    slc = get(mm, bgn, end)
    return json.loads(slc)
