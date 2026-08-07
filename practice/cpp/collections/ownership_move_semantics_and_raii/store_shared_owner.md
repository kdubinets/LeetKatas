# Name

Store a Shared Owner

# Description

Append a const `std::shared_ptr<Resource>` to a vector so the vector entry becomes an additional owner of the same object. This exercise covers copying shared ownership to extend resource lifetime.

# Solution

```cpp
owners.push_back(owner);
```
