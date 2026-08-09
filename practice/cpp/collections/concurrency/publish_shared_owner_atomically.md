# Name

Publish Shared Ownership Atomically

# Description

Transfer a supplied shared owner into an atomic smart-pointer slot using release ordering. Readers that acquire-load the slot can safely share the immutable string and observe initialization performed before publication. This covers the C++20 atomic `shared_ptr` specialization.

# Solution

```cpp
slot.store(std::move(value), std::memory_order_release);
```
