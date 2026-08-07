# Name

Move-Assign a Handle

# Description

Complete move assignment for a non-copyable RAII type whose valid handles are not `-1`. Handle self-assignment, release this object's current handle, transfer the source handle, invalidate the source, and return `*this`. This exercise covers safe move assignment of a scalar resource handle.

# Solution

```cpp
if (this != &other) {
    if (value_ != -1) {
        release_handle(value_);
    }
    value_ = std::exchange(other.value_, -1);
}
return *this;
```
