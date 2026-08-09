# Name

Insert After the Forward-List Head Position

# Description

Insert every integer from the read-only `source` span before the current first node of `destination`, preserving source order and all existing destination order. This exercise covers the conceptual before-first position and iterator-range insertion of `std::forward_list`.

# Solution

```cpp
destination.insert_after(destination.before_begin(), source.begin(), source.end());
```
