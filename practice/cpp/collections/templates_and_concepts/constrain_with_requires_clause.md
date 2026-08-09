# Name

Constrain with a Requires Clause

# Description

Define `add` for two forwarding-reference parameters and place a trailing requires-clause on it. The overload is viable only when removing cv-reference qualification from both deduced types produces the same type. Preserve each argument's value category in the addition expression.

# Solution

```cpp
auto add(Left&& left, Right&& right)
    requires std::same_as<std::remove_cvref_t<Left>, std::remove_cvref_t<Right>> {
    return std::forward<Left>(left) + std::forward<Right>(right);
}
```
