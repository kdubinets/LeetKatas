# Name

Write Exact Bytes

# Description

Write every byte from a read-only `std::span<const std::byte>` to a caller-provided `std::ostream&`, then return whether the stream remains successful. The span size is representable as `std::streamsize`; callers use a binary-mode file stream when platform text translation must not occur. This exercise covers bounded unformatted output and stream-state validation.

# Solution

```cpp
auto count = static_cast<std::streamsize>(source.size());
output.write(reinterpret_cast<const char*>(source.data()), count);
return static_cast<bool>(output);
```
