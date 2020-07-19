from unittest.main import main
from lazy_json import file
import mmap
import unittest
from unittest import skip


"""
{
    "one": {
        "two": 2
    },
    "three": 3,
    "another": "and so i said \"hahaha\"!",
    "big_number": -3.14159,
    "boolean": true,
    "empty": null
}
"""


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

    def test_get_next_char_at_pos_gt_0(self):
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

    def test_end_of_json_obj_true(self):
        mm = MM
        pos = 31
        gold = True
        output = file.end_of_json_obj(mm, pos)
        self.assertEqual(gold, output)

    def test_end_of_json_obj_false(self):
        mm = MM
        pos = 40
        gold = False
        output = file.end_of_json_obj(mm, pos)
        self.assertEqual(gold, output)

    def test_val_is_json_obj_true(self):
        mm = MM
        pos = 13
        gold = True
        output = file.val_is_json_obj(mm, pos)
        self.assertEqual(gold, output)

    def test_val_is_json_obj_false(self):
        mm = MM
        pos = 30
        gold = False
        output = file.val_is_json_obj(mm, pos)
        self.assertEqual(gold, output)

    def test_seek_to_key(self):
        mm = MM
        pos = 0
        gold = 6
        output = file.seek_to_key(mm, pos)
        self.assertEqual(gold, output)

    def test_seek_to_val(self):
        mm = MM
        pos = 10
        gold = 13
        output = file.seek_to_val(mm, pos)
        self.assertEqual(gold, output)

    def test_get_key(self):
        mm = MM
        pos = 6
        gold = file.bound(6, 11)
        output = file.get_key(mm, pos)
        self.assertEqual(gold, output)

    def test_get_val_string(self):
        mm = MM
        pos = 70
        gold = file.bound(70, 97)
        output = file.get_val(mm, pos)
        self.assertEqual(gold, output)

    def test_get_val_int(self):
        mm = MM
        pos = 30
        gold = file.bound(30, 31)
        output = file.get_val(mm, pos)
        self.assertEqual(gold, output)

    def test_get_val_float(self):
        mm = MM
        pos = 117
        gold = file.bound(117, 125)
        output = file.get_val(mm, pos)
        self.assertEqual(gold, output)

    def test_get_val_bool(self):
        mm = MM
        pos = 142
        gold = file.bound(142, 146)
        output = file.get_val(mm, pos)
        self.assertEqual(gold, output)
    
    def test_get_val_null(self):
        mm = MM
        pos = 161
        gold = file.bound(161, 165)
        output = file.get_val(mm, pos)
        self.assertEqual(gold, output)

    def test_count_between_matches(self):
        mm = MM
        sub = "o"
        bgn = 0
        end = 30
        gold = 2
        output = file.count_between(mm, sub, bgn, end)
        self.assertEqual(gold, output)

    def test_count_between_no_matches(self):
        mm = MM
        sub = "foo"
        bgn = 0
        end = 30
        gold = 0
        output = file.count_between(mm, sub, bgn, end)
        self.assertEqual(gold, output)

    def test_find_end_of_json_whole(self):
        mm = MM
        pos = 0
        gold = 166
        output = file.find_end_of_json(mm, pos)
        self.assertEqual(gold, output)

    def test_find_end_of_json_nested(self):
        mm = MM
        pos = 13
        gold = 36
        output = file.find_end_of_json(mm, pos)
        self.assertEqual(gold, output)

    def test_get_json_from_bound(self):
        mm = MM
        b = file.bound(6, 11)
        gold = "one"
        output = file.get_json_from_bound(mm, b)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
