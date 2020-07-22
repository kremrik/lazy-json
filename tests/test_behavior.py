from lazy_json import lazy_json
import unittest


with open("/home/kemri/Projects/lazy-json/file_examples/nested.json", "r") as i:
    NESTED = lazy_json.load(i)

with open("/home/kemri/Projects/lazy-json/file_examples/numbers.json", "r") as j:
    NUMBERS = lazy_json.load(j)


class test_lazy_json(unittest.TestCase):

    def test_get_item(self):
        data = NESTED
        gold = 3
        output = data["three"]
        self.assertEqual(gold, output)

    def test_get_nested_item(self):
        data = NESTED
        gold = 2
        output = data["one"]["two"]
        self.assertEqual(gold, output)

    def test_keys(self):
        data = NESTED
        gold = ["one", "three", "another", "big_number", "boolean", "empty"]
        output = list(data.keys())
        self.assertEqual(gold, output)

    def test_values(self):
        # NOTE: cannot determine equality of generators without yielding
        #  all values, so the comparison will be between non-nested vals
        data = NUMBERS
        gold = [1, 2]
        output = list(data.values())
        self.assertEqual(gold, output)

    def test_items(self):
        # NOTE: cannot determine equality of generators without yielding
        #  all values, so the comparison will be between non-nested vals
        data = NUMBERS
        gold = [("one", 1), ("two", 2)]
        output = list(data.items())
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
