# Name

Downcast a Shared Owner

# Description

Given shared ownership through polymorphic `Base`, return `std::shared_ptr<Derived>` sharing the same object and control block when the dynamic type is compatible. Return an empty shared pointer when it is not. This exercise covers checked polymorphic conversion of shared ownership.

# Solution

```cpp
return std::dynamic_pointer_cast<Derived>(owner);
```
