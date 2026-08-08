# Name

Translate an Exception to a Result

# Description

Call a declared integer-producing operation and return its value on success. Translate any `std::exception` failure into a string error containing `what()` without catching unrelated nonstandard exceptions.

# Solution

```cpp
try {
    return read_value();
} catch (const std::exception& error) {
    return std::string{error.what()};
}
```
