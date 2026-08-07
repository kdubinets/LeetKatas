# Name

Replace a Unique Resource

# Description

Replace the resource held by a mutable `std::unique_ptr<Resource>` with a newly constructed resource carrying the supplied ID. Any previous resource must be cleaned up automatically. This exercise covers safe replacement of exclusive ownership.

# Solution

```cpp
owner = std::make_unique<Resource>(id);
```
