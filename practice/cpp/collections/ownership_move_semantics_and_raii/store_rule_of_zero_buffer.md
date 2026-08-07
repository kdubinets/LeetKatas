# Name

Store a Rule-of-Zero Buffer

# Description

Choose the private member type for `Buffer` so it owns `int` elements, can be constructed with a runtime size, and automatically receives correct copy, move, and destruction behavior without declaring special members. This exercise covers rule-of-zero composition with a standard owning container.

# Solution

```cpp
std::vector<int> data_;
```
