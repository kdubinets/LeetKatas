# Name

Append Strings by Moving

# Description

Append the strings from a mutable source vector to a distinct mutable destination vector in their current order by moving each string rather than copying it. The source vector retains its size, but its elements may be left in valid unspecified states. This exercise covers move iterators over a container range.

# Solution

```cpp
destination.insert(destination.end(),
                   std::make_move_iterator(source.begin()),
                   std::make_move_iterator(source.end()));
```
