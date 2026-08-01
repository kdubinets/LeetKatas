# Name

Add to All Map Values

# Description

Mutate an ordered integer map by adding a supplied offset to every mapped value while leaving all keys unchanged. This exercise covers modifying the mutable second field of associative entries whose first field is const.

# Solution

```cpp
for (auto& entry : values) {
    entry.second += offset;
}
```
