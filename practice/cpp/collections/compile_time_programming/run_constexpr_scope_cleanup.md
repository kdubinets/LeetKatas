# Name

Run Constexpr Scope Cleanup

# Description

Define the `ScopeIncrement` destructor so it increments the referenced integer when the guard leaves scope and can execute during constant evaluation. The supplied immediate function verifies one deterministic cleanup. This covers C++20 constexpr destructors.

# Solution

```cpp
constexpr ~ScopeIncrement() {
    ++*count;
}
```
