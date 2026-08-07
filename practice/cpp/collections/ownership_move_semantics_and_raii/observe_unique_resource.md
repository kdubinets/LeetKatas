# Name

Observe a Unique Resource

# Description

Return a nullable raw pointer to the object held by a const `std::unique_ptr<Resource>` without changing or sharing its ownership. This exercise covers obtaining a non-owning observer from an exclusive owner.

# Solution

```cpp
return owner.get();
```
