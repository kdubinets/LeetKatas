# Name

Consume a String View Prefix

# Description

For a valid count, return a view of the first `count` characters and advance the mutable input view past them. No characters may be copied. This exercise covers fixed-width parsing by pairing prefix slicing with view advancement.

# Solution

```cpp
auto prefix = remaining.substr(0, count);
remaining.remove_prefix(count);
return prefix;
```
