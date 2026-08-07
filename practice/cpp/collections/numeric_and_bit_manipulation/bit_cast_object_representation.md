# Name

Copy an Object Representation

# Description

Return the object representation of a `double` as a same-sized `std::array<std::byte>` without numeric conversion or aliasing through an incompatible pointer. The byte order is the platform's native representation. This exercise covers copying bits safely between equally sized trivially copyable types.

# Solution

```cpp
return std::bit_cast<std::array<std::byte, sizeof(double)>>(value);
```
