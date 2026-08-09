# Name

Erase After a Forward-List Predecessor

# Description

Remove the existing node immediately after `predecessor` from a mutable `std::forward_list<int>` and return the following position, which may be the end iterator. The predecessor may be the list's conceptual before-first position. This exercise covers predecessor-based forward-list erasure and its returned continuation iterator.

# Solution

```cpp
return values.erase_after(predecessor);
```
