# Name

Transfer a Unique Owner

# Description

Move ownership between two distinct `std::unique_ptr<Resource>` objects. The destination's previously owned resource must be cleaned up, and the source must become empty. This exercise covers move assignment of exclusive ownership.

# Solution

```cpp
destination = std::move(source);
```
