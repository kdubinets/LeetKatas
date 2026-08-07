# Name

Move-Construct a Handle

# Description

Complete the move constructor for a small RAII type whose valid scalar handles are not `-1`. Transfer the handle into the new object and atomically replace the source handle with `-1` so only one destructor releases it. This exercise covers move construction for a non-copyable resource handle.

# Solution

```cpp
: value_(std::exchange(other.value_, -1)) {}
```
