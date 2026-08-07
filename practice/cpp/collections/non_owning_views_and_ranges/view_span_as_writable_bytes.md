# Name

View a Span as Writable Bytes

# Description

Expose the object representations of a mutable `std::span<std::uint32_t>` as writable bytes without copying storage. This exercise covers producing a mutable byte view from mutable contiguous objects.

# Solution

```cpp
return std::as_writable_bytes(values);
```
