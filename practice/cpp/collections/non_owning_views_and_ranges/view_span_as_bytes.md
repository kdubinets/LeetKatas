# Name

View a Span as Bytes

# Description

Expose the complete object representations of a read-only span of `std::uint32_t` as a non-owning `std::span<const std::byte>`. The source objects must not be copied or made writable. This exercise covers safe byte-level viewing of contiguous objects.

# Solution

```cpp
return std::as_bytes(values);
```
