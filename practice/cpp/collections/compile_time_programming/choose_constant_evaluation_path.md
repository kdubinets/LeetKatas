# Name

Choose the Evaluation Path

# Description

Return `1` when `selected_value` is being evaluated as a constant expression; otherwise return the result of the supplied non-constexpr runtime function. This trains C++20 evaluation-context detection while keeping one function usable in both contexts.

# Solution

```cpp
if (std::is_constant_evaluated()) {
    return 1;
}
return runtime_value();
```
