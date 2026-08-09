# Name

Consume Shared Ownership Atomically

# Description

Acquire-load a possibly empty shared owner from the supplied atomic smart-pointer slot and return it. A non-null result must extend the immutable string's lifetime and observe initialization sequenced before the matching release publication.

# Solution

```cpp
return slot.load(std::memory_order_acquire);
```
