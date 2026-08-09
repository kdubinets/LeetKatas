# Name

Dispatch a Constexpr Virtual Call

# Description

Override the const virtual `value` function in `Derived` so it returns the stored integer and remains usable during constant evaluation. The supplied immediate function calls it through a base reference, exercising C++20 constant-evaluated virtual dispatch.

# Solution

```cpp
constexpr int value() const override {
    return value_;
}
```
