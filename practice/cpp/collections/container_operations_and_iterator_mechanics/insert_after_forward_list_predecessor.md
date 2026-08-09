# Name

Insert After a Forward-List Predecessor

# Description

Insert `value` immediately after the valid `predecessor` position in a mutable `std::forward_list<int>` and return an iterator to the inserted node. The predecessor may be the list's conceptual before-first position. This exercise covers predecessor-based forward-list insertion.

# Solution

```cpp
return values.insert_after(predecessor, value);
```
