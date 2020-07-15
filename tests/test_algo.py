from lazy_json.core import *
import unittest
from unittest import skip
from functools import partial


@skip("no longer in use")
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

        gold = boundary(0, 6)
        output = string_bound(find, get, tell)
        self.assertEqual(gold, output)

    def test_simple_with_more_quotes(self):
        inpt = r'"value", "key": "another"'

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def get(x):
            return inpt[x]
        def tell():
            return 0

        gold = boundary(0, 7)
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

        gold = boundary(2, 18)
        output = string_bound(find, get, tell)
        self.assertEqual(gold, output)


class test_number_bound(unittest.TestCase):

    def test_int(self):
        inpt = r'1, '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def tell():
            return 0

        gold = boundary(0, 1)
        output = number_bound(find, tell)
        self.assertEqual(gold, output)

    def test_long_int(self):
        inpt = r' 12345, '

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def tell():
            return 1

        gold = boundary(1, 6)
        output = number_bound(find, tell)
        self.assertEqual(gold, output)


class test_parse_schema(unittest.TestCase):

    def test_single_obj(self):
        inpt = r'{"foo":"bar"}'
        gold = [
            (boundary(1, 5), boundary(8, 13))
        ]

        def find(x, start=None, end=None):
            return inpt.find(x, start, end)
        def get(x):
            return inpt[x]
        def tell():
            return 0
        def seek(x):
            return None


if __name__ == "__main__":
    unittest.main()
