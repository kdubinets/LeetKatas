# Name

Drop a Shared Owner

# Description

Reset one mutable `std::shared_ptr<Resource>` so it no longer owns the object. Other shared owners, if present, must remain valid; destroy the resource only when this was the last owner. This exercise covers relinquishing one shared-ownership stake.

# Solution

```cpp
owner.reset();
```
