# Name

Run Callbacks in Order

# Description

Invoke every non-empty callback in a const vector from first to last. The vector and its callable objects must not be replaced or reordered; all entries are guaranteed to contain targets.

# Solution

```cpp
for (const auto& callback : callbacks) {
    callback();
}
```
