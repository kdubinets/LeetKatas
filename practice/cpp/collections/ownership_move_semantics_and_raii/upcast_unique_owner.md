# Name

Upcast a Unique Owner

# Description

Convert a by-value `std::unique_ptr<Derived>` into `std::unique_ptr<Base>` while preserving the same dynamically allocated object and exclusive ownership. The base has a virtual destructor so eventual destruction remains correct. This exercise covers polymorphic transfer through a converting unique-pointer move.

# Solution

```cpp
return owner;
```
