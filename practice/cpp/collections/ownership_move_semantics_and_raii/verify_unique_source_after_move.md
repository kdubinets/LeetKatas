# Name

Verify a Unique Source After Move

# Description

Given a nonempty `std::unique_ptr<Resource>`, move it into a local owner and return whether the source is empty and the destination is nonempty. The local owner cleans up at function exit. This exercise covers the specified moved-from state of exclusive smart pointers.

# Solution

```cpp
auto destination = std::move(source);
return source == nullptr && destination != nullptr;
```
