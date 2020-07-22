# lazy-json

## Branch combined-ideas notes
#### WHAT HAPPENED?
Figured out that attempting to perform a direct-access read of a JSON file was going to prove impossible without
performing crazy regex/tests for whether a desired key is _actually_ a key, or simply part of a string value.
That was branch `direct-access`.
However, in the process of determining this, we figured out how to find the end of an arbitrarily nested value.
Previously, in branch `file-layer`, we couldn't figure out how to recursively yield generators because we
couldn't find the end of a nested value (ie, we recursed immediately and lost the "end" position of the value).
So we used that learning and combined it with the previously built generator behavior for `lazy_json` and
arrived at the working product.

#### UPDATE
Turns out that `mmap` doesn't play nicely with _actual_ memory IRL, and memory spikes when searching through a 
huge mmap file. However, we can fix this with a sliding window using `mmap`'s `length` and `offset` args.

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
