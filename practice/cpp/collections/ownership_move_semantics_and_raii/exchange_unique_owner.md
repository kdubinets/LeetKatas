# Name

Exchange a Unique Owner

# Description

Take and return the `std::unique_ptr<Resource>` stored in a mutable owner while replacing it with null as one exchange operation. This exercise covers combining move extraction and defined replacement for a move-only value.

# Solution

```cpp
return std::exchange(owner, nullptr);
```
