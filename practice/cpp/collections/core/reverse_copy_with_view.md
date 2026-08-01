# Name

Reverse Copy Through a View

# Description

Copy a const integer vector into a new vector in reverse order while leaving the input unchanged. The result capacity is already reserved. This exercise covers reversing traversal lazily with a C++20 view and materializing it through an output iterator.

# Solution

```cpp
auto reversed = values | std::views::reverse;
std::ranges::copy(reversed, std::back_inserter(result));
```
