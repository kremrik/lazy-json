# lazy-json
A test project to explore Python's `mmap` library and the complexities of parsing a recursive data format "in stream"

## Design goals
`lazy_json` allows you to treat arbitrarily large JSON files on disk as a streaming problem rather than a batch problem.
It lazily generates key/value pairs of the object such that parsing is bound by CPU rather than memory or IO.

### Example
Suppose you have a JSON file consisting of 10,000,000 key/value pairs such that each field is ~100 bytes. 
No one knows why this object exists, it just does. And on disk it's almost 5gb. You know that you need 
the value at key "000314159" but you can't retrieve it by loading into memory with the `json` library
because your computer sucks and only has 4gb of RAM. `lazy_json` to the rescue:

```python
import lazy_json

with open("really_big.json", "w") as j:
    data = lazy_json.load(j)

data["000314159"]
# b'\x1f\x8b\x08\x00W\x14\n_\x02\xff30006414\xb5\x04\x00\x89l\xed\\\t\x00\x00\x00...'
```

Treating JSON like a stream process:
```python
with open("really_big.json", "w") as j:
    data = lazy_json.load(j)

data.items()
# <generator object ljson.items at 0x7f7708cb2f20>

for k, v in data.items():
    print({k: v})
# {'one': 1}
# {'two': 2}
# ...
```

Nested JSON is handled such that the key is returned as a string, but the value is itself a `lazy_json` object.
This allows you to do things like this:

`nested.json`
```json
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
```

```python
with open("nested.json", "w") as j:
    data = lazy_json.load(j)

data["one"]["two"]
# 2
```

Keep in mind that, since this process is treated as a stream, the further "down" the file you go, the longer the
process will take to materialize values. The easiest way forward to solve this would be to simply seek to the
place in the file where a key is found, and repeat the process for each sub-key in the slice. This would require
a different mmnap traversal that resets itself after N characters to avoid the aforementioned weird "mem leak".
I don't feel like implementing this right now, but it's certainly possible.

### Test it Yourself
Creates a really simple file like:
```json
{
    "000000001": "hellohellohello...",
    "000000002": "hellohellohello...",
    ...
    ...
}
```

```python
def write_json(lines, value): 
    with open("huge.json", "w") as j: 
        j.write("{") 
        for i in range(lines): 
            j.write(make_json_kv(str(i).zfill(len(str(lines))), value) + ",") 
            j.write(make_json_kv(str(i+1).zfill(len(str(lines))), value)) 
            j.write("}") 

def make_json_kv(key, val): 
    return f'"{key}": "{val}"'

write_json(100000000, "hello"*100)
```
