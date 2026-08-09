# Name

Require a Non-Throwing Expression

# Description

Define `NothrowReset<T>` with a compound requirement that accepts a mutable `T` only when `reset()` is both well-formed and declared non-throwing.

# Solution

```cpp
concept NothrowReset = requires(T& value) {
    { value.reset() } noexcept;
};
```
