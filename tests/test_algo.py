from lazy_json.core import json_generator
import unittest
from unittest import skip


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


if __name__ == "__main__":
    unittest.main()
