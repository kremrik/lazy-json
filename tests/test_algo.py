from lazy_json.core import *
import unittest
from unittest import skip
from functools import partial


class test_generator(unittest.TestCase):

    def test_one_kv(self):
        json_stream = '{"foo":1}'
        j_gen = json_generator(json_stream)
        
        gold = [{"foo": 1}]
        output = list(j_gen)
        self.assertEqual(gold, output)

    def test_two_kvs(self):
        # if we get to a comma and have an unmatched open brace, we make up a
        # closing brace to add to the output, and yield that. if we get to a 
        # closing brace, we pop off the corresponding opening brace 
        json_stream = '{"foo":1,"bar":2,"baz":3}'
        j_gen = json_generator(json_stream)
        
        gold = [{"foo": 1}, {"bar": 2}, {"baz":3}]
        output = list(j_gen)
        self.assertEqual(gold, output)

    def test_ignore_whitespace(self):
        # if we get to a comma and have an unmatched open brace, we make up a
        # closing brace to add to the output, and yield that. if we get to a 
        # closing brace, we pop off the corresponding opening brace 
        json_stream = '{\n\t"foo": 1,\n\t"bar": 2,\n\t"baz": 3\n}'
        j_gen = json_generator(json_stream)
        
        gold = [{"foo": 1}, {"bar": 2}, {"baz":3}]
        output = list(j_gen)
        self.assertEqual(gold, output)


class test_string_bound(unittest.TestCase):

    def test_simple(self):
        inpt = r'"test", '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def get(x):
            return inpt[x]
        def tell():
            return 0

        gold = value_bound(0, 5)
        output = string_bound(find, get, tell)
        self.assertEqual(gold, output)

    def test_escaped_quote(self):
        inpt = r': "i said \"wow\"", '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def get(x):
            return inpt[x]
        def tell():
            return 2

        gold = value_bound(2, 17)
        output = string_bound(find, get, tell)
        self.assertEqual(gold, output)


class test_number_bound(unittest.TestCase):

    def test_int(self):
        inpt = r'1, '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def tell():
            return 0

        gold = value_bound(0, 1)
        output = number_bound(find, tell)
        self.assertEqual(gold, output)

    def test_long_int(self):
        inpt = r' 12345, '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def tell():
            return 1

        gold = value_bound(1, 6)
        output = number_bound(find, tell)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
