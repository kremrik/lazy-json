from unittest.main import main
from lazy_json import file
from lazy_json import lazy_json
import mmap
import unittest


with open("/home/kemri/Projects/lazy-json/file_examples/numbers.json", "r") as j:
    NUMBERS = mmap.mmap(
        j.fileno(), 
        0,
        access=mmap.ACCESS_READ
        )
DATA = lambda: NUMBERS


class test_walk_json(unittest.TestCase):

    def test_no_nesting_numbers(self):
        data = DATA
        gold = [
            (file.bound(1, 6), file.bound(8, 9)),
            (file.bound(11, 16), file.bound(18, 19))
        ]
        output = list(lazy_json.walk_json(data, 0, 19))
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
