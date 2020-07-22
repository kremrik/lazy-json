# lazy-json

## Design goals
`lazy-json` is a utility that solves a problem you hope never to have: a JSON file that's too large to load in memory. 
I don't know what kind of monster would create such a file, but this is an exercise in solving the interesting problem
surrounding large, recursive data formats. 

### Example
Suppose you have a JSON file consisting of 100,000,000 key/value pairs such that each field is 100 bytes. 
No one knows why this object exists, it just does. And on disk it's almost 10gb. You know that you need 
the value at key "000314159" but you can't retrieve it by loading into memory with the `json` library
since your computer only has 8gb of RAM. `lazy-json` to the rescue:

```python
import lazy_json

with open("really_big.json", "w") as j:
    data = lazy_json.load(j)

data["000314159"]
# b'\x1f\x8b\x08\x00W\x14\n_\x02\xff30006414\xb5\x04\x00\x89l\xed\\\t\x00\x00\x00...'
```

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
