# Name

Make a Shared Record

# Description

Construct a `Record` from an integer ID and return shared ownership of it. Allocate the object and ownership bookkeeping together through the standard shared-construction facility. This exercise covers efficient creation of a `std::shared_ptr`.

# Solution

```cpp
return std::make_shared<Record>(id);
```
