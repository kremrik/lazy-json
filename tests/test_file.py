from unittest.main import main
from lazy_json import file
import mmap
import unittest
from unittest import skip


with open("/home/kemri/Projects/lazy-json/file_examples/nested.json", "r") as j:
    MM = mmap.mmap(
        j.fileno(), 
        0,  # not sure if this is wise
        access=mmap.ACCESS_READ
        )


class test_primitives(unittest.TestCase):

    def test_find(self):
        mm = MM
        char = '"'
        gold = 6
        output = file.find(mm, char)
        self.assertEqual(gold, output)

    def test_get(self):
        mm = MM
        start = 0
        gold = "{"
        output = file.get(mm, start)
        self.assertEqual(gold, output)


class test_combinations(unittest.TestCase):

    def test_get_next_char_at_pos_0(self):
        mm = MM
        pos = 0
        char = '{'
        gold = file.mmap_result(0, 0)
        output = file.get_next_char(mm, pos, char)
        self.assertEqual(gold, output)

    def test_get_next_char_at_pos_gt_o(self):
        mm = MM
        pos = 1
        char = '{'
        gold = file.mmap_result(13, 13)
        output = file.get_next_char(mm, pos, char)
        self.assertEqual(gold, output)

    def test_get_next_unescaped_char_at_pos_0(self):
        mm = MM
        pos = 0
        char = '"'
        gold = file.mmap_result(6, 6)
        output = file.get_next_unescaped_char(mm, pos, char)
        self.assertEqual(gold, output)

    def test_get_next_unescaped_char_with_char_to_escape(self):
        mm = MM
        pos = 90
        char = '"'
        gold = file.mmap_result(96, 96)
        output = file.get_next_unescaped_char(mm, pos, char)
        self.assertEqual(gold, output)

    def test_get_next_non_whitespace_char_at_pos_0(self):
        mm = MM
        pos = 0
        gold = file.mmap_result("{", 0)
        output = file.get_next_non_whitespace_char(mm, pos)
        self.assertEqual(gold, output)

    def test_get_next_non_whitespace_char_at_pos_gt_0(self):
        mm = MM
        pos = 1
        gold = file.mmap_result('"', 6)
        output = file.get_next_non_whitespace_char(mm, pos)
        self.assertEqual(gold, output)

    def test_get_prev_non_whitespace_char_at_pos_0(self):
        mm = MM
        pos = 0
        gold = file.mmap_result(None, -1)
        output = file.get_prev_non_whitespace_char(mm, pos)
        self.assertEqual(gold, output)

    def test_get_prev_non_whitespace_char_at_pos_gt_0(self):
        mm = MM
        pos = 13
        gold = file.mmap_result(':', 11)
        output = file.get_prev_non_whitespace_char(mm, pos)
        self.assertEqual(gold, output)


class test_schemes(unittest.TestCase):

    def test_get_key_bound(self):
        mm = MM
        pos = 0
        gold = file.bound(7, 10)
        output = file.get_key_bound(mm, pos)
        self.assertEqual(gold, output)

    def test_get_value_bound_string(self):
        mm = MM
        pos = 68
        gold = file.bound(71, 96)
        output = file.get_value_bound(mm, pos)
        self.assertEqual(gold, output)

    def test_get_value_bound_int(self):
        mm = MM
        pos = 28
        gold = file.bound(30, 31)
        output = file.get_value_bound(mm, pos)
        self.assertEqual(gold, output)

    def test_get_value_bound_float(self):
        mm = MM
        pos = 115
        gold = file.bound(117, 125)
        output = file.get_value_bound(mm, pos)
        self.assertEqual(gold, output)

    def test_get_value_bound_bool(self):
        mm = MM
        pos = 140
        gold = file.bound(142, 146)
        output = file.get_value_bound(mm, pos)
        self.assertEqual(gold, output)
    
    def test_get_value_bound_null(self):
        mm = MM
        pos = 159
        gold = file.bound(161, 165)
        output = file.get_value_bound(mm, pos)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
