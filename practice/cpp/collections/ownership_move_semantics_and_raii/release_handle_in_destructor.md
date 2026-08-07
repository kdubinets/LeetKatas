# Name

Release a Handle in the Destructor

# Description

Complete the destructor of a non-copyable handle wrapper. Call the supplied release function exactly when the stored scalar handle is valid, represented by any value other than `-1`. This exercise covers deterministic cleanup of a non-memory resource.

# Solution

```cpp
if (value_ != -1) {
    release_handle(value_);
}
```
