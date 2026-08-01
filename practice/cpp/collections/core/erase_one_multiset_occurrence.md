# Name

Erase One Multiset Occurrence

# Description

Remove exactly one occurrence of an integer from a mutable `std::multiset<int>` and return whether a matching occurrence existed. Other equal occurrences must remain. This exercise covers iterator-based multiset erasure rather than key-based removal of every match.

# Solution

```cpp
auto it = values.find(target);
if (it == values.end()) {
    return false;
}
values.erase(it);
return true;
```
