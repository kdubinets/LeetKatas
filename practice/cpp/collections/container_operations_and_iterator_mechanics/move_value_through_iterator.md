# Name

Move a Value Through an Iterator

# Description

In a generic operation, construct and return the iterator's value type from the element at the dereferenceable `position`. Access that element through the C++20 move-aware iterator customization point so proxy and specialized iterator behavior can participate. The constraints ensure the owning result can be constructed from the iterator's rvalue-reference type. This exercise covers customization-aware movement in iterator-generic code.

# Solution

```cpp
return std::ranges::iter_move(position);
```
