# Name

Make a Unique Record

# Description

Construct a `Record` from a const string name and integer score and return it under exclusive `std::unique_ptr` ownership. This exercise covers direct, exception-safe construction of one exclusively owned object.

# Solution

```cpp
return std::make_unique<Record>(name, score);
```
