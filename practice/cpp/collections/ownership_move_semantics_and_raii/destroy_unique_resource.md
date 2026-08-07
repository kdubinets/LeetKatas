# Name

Destroy a Unique Resource

# Description

Immediately destroy the object, if any, held by a mutable `std::unique_ptr<Resource>` and leave the pointer empty. This exercise covers explicitly ending exclusive ownership before the owner's own scope ends.

# Solution

```cpp
owner.reset();
```
