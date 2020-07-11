from json import loads
from queue import deque
from typing import Generator


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
