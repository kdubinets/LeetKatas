# Name

Drain Stack to Vector

# Description

Remove every integer from a mutable `std::stack<int>` and return them in a vector ordered from the original top down to the original bottom. This exercise covers repeated stack access and removal.

# Solution

```cpp
while (!values.empty()) {
    result.push_back(values.top());
    values.pop();
}
```
