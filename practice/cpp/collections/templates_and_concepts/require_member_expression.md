# Name

Require a Member Expression

# Description

Define `HasClear<T>` with a requires-expression that introduces a mutable `T` reference and verifies that `value.clear()` is a valid expression.

# Solution

```cpp
concept HasClear = requires(T& value) {
    value.clear();
};
```
