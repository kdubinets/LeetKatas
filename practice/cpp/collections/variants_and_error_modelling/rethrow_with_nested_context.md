# Name

Rethrow with Nested Context

# Description

Run a declared settings operation. If it throws, add the runtime-error message `loading settings failed` while preserving the current exception as its nested cause.

# Solution

```cpp
try {
    load_settings();
} catch (...) {
    std::throw_with_nested(std::runtime_error{"loading settings failed"});
}
```
