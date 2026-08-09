# Name

Write with an Exclusive Lock

# Description

Replace an integer protected by the supplied shared mutex while holding exclusive lock ownership. The operation must exclude both other writers and shared readers for the mutation.

# Solution

```cpp
std::unique_lock lock(mutex);
value = replacement;
```
