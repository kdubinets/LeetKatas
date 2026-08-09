# Name

Copy into a Forward List with a Front Inserter

# Description

Copy the integers from the const source vector in forward traversal order into the front of an existing `std::forward_list<int>`. Each copied value becomes the new first element, so the inserted prefix appears in reverse source order while the previous destination sequence remains as the suffix. This exercise covers adapting an algorithm's output to a destination that provides front insertion rather than append.

# Solution

```cpp
std::copy(source.begin(), source.end(), std::front_inserter(destination));
```
