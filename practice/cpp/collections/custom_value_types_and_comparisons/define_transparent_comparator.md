# Name

Define a Transparent Comparator

# Description

Define an ordering policy for owning `Name` values that also compares either operand against `std::string_view`. Mark the policy for heterogeneous associative lookup and order every supported pair by the same text representation.

# Solution

```cpp
using is_transparent = void;
bool operator()(const Name& left, const Name& right) const { return left.value < right.value; }
bool operator()(const Name& left, std::string_view right) const { return left.value < right; }
bool operator()(std::string_view left, const Name& right) const { return left < right.value; }
```
