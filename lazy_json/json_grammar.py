from lazy_json import file
import mmap
from typing import Callable


def parse_json():
    pass


def parse_kv(
    next_char: Callable,
    next_unescaped: Callable,
    next_nonwhitespace: Callable
):
    key_bgn = next_char('"')
    key_end = next_char(":") - 1

    val_bgn = next_nonwhitespace()
    
    
