from collections import namedtuple
from json import loads
from queue import deque
from typing import Callable, Generator


boundary = namedtuple("boundary", ["bgn", "end"])


def json_generator(
    json_stream
) -> Generator:
    """
    How to find a key
    -----------------
    A string, in quotes, preceded by (sans whitespace) either of the following: 
    - `{` 
    - `,`
    And terminated by:
    - `:`

    How to find a value
    -------------------
    Any object following a `:`
    """
    syntax = r'{},'
    whitespace = [" ", "\n", "\t"]
    
    json_schema = deque()
    json_obj = deque()

    for char in json_stream:
        if char in whitespace:
            continue

        if char not in syntax:
            json_obj.append(char)
            continue

        if char == "{":
            json_schema.append(char)
            json_obj.append(char)
        elif char == "}":
            json_obj.append(char)
            kv_pair = "".join(json_obj)
            json_obj.clear()
            yield loads(kv_pair)
        elif char == ",":
            json_obj.append("}")
            kv_pair = "".join(json_obj)
            json_obj.clear()
            json_obj.append("{")
            yield loads(kv_pair)


def get_value_type(
    string: str
) -> str:
    if string in "+-.0123456789":
        return "number"
    if string == '"':
        return "string"
    if string in "tf":
        return "boolean"
    if string == "n":
        return "null"


def key_bound(
    find: Callable,
    get: Callable,
    tell: Callable
) -> boundary:
    return string_bound(
        find=find,
        get=get,
        tell=tell
    )


def value_bound(
    find: Callable,
    get: Callable,
    tell: Callable
) -> boundary:
    bound_map = {
        "number": lambda: number_bound(find, tell),
        "string": lambda: string_bound(find, get, tell),
        "boolean": None,
        "null": None
    }

    value_type = get_value_type(get(tell()))
    return bound_map[value_type]()


# TODO: higher-order find/get must keep track (somehow) of where they've aready been 
#  because otherwise something like `find` will just go to the earliest value.
#  the good news is that the `boundary` object returned contains the data needed
#  to set the NEXT seek start bound.
def string_bound(
    find: Callable,
    get: Callable,
    tell: Callable
) -> boundary:
    bgn = tell()
    nxt = find(r'"', bgn + 1)
    nxt_prev = get(nxt - 1)

    end_of_string = False

    while not end_of_string:
        if nxt_prev == "\\":
            nxt = find(f'"', nxt + 1)
            nxt_prev = get(nxt - 1)
        else:
            end_of_string = True

    return boundary(bgn, nxt + 1)


def number_bound(
    find: Callable,
    tell: Callable
) -> boundary:
    bgn = tell()
    end = None

    next_comma = find(",")
    next_brace = find("}")
    minimum = min(next_comma, next_brace)
    maximum = max(next_comma, next_brace)
    end = minimum if minimum > 0 else maximum

    return boundary(bgn, end)
