# Name

Return a Lazy Scaled View

# Description

Return a lazy view over a const integer vector that produces each value multiplied by `factor` using `long long` arithmetic. Capture the factor by value, do not materialize the result, and leave ownership of the input with the caller, which must outlive the returned view. This exercise covers returning a composed non-owning transform view with safe callable state.

# Solution

```cpp
return values | std::views::transform([factor](int value) {
    return static_cast<long long>(value) * factor;
});
```
