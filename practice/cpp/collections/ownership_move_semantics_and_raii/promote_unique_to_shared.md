# Name

Promote Unique Ownership to Shared

# Description

Convert a by-value `std::unique_ptr<Resource>` into `std::shared_ptr<Resource>`, transferring the same object rather than allocating or copying another one. This exercise covers the one-way transition from exclusive to shared ownership.

# Solution

```cpp
return std::shared_ptr<Resource>{std::move(owner)};
```
