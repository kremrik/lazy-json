# lazy-json

## Branch file-layer notes
WHAT HAPPENED?
--------------
It currently doesn't seem possible to me to yield k/v pairs where v could be a
generator itself due to the fact that we would need to call all of its values
to determine where the end of the line is (all that just to know how to move to
the next non-nested key).

WHAT DID WE LEARN?
------------------
That we could recursively yield our way through every single key/value in a
JSON object, but would have to find a way to track the parent key in doing
that (so the user wouldn't get lost while iterating).
We also learned how to layer the design to such an extent that all of `parse`
utilized only the schemes level of the `file` layer. `wrapper` made a call to a
lower level, but that could probably be fixed easily and quickly if we wanted
to follow the letter of the law there.

WHERE COULD THIS GO NEXT?
-------------------------
We could implement a generator such that the user could simply iterate through
every single k/v pair, including nested ones, without being able to skip said
nested values. It would require a way to track the parent key, just to prevent 
the user from getting lost in navigation. Would just need to use `yield from`.

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

old_val = data["000314159"]  # result is cached so the call is not made again
new_val = "REMOVED"
data["000314159"] = new_val
```
