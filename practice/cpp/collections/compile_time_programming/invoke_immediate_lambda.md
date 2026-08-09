# Name

Invoke an Immediate Lambda

# Description

Define `answer` as a constant initialized by calling a lambda whose invocation is required to occur during constant evaluation. The lambda must return the product of `6` and `7`. This isolates C++20 immediate-lambda syntax.

# Solution

```cpp
constexpr int answer = []() consteval { return 6 * 7; }();
```
