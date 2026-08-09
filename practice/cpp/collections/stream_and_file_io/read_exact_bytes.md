# Name

Read Exact Bytes

# Description

Read exactly `destination.size()` bytes from a caller-provided `std::istream&` into mutable `std::span<std::byte>` storage. Return whether the requested byte count was transferred; a short read returns false while retaining any bytes that were obtained. The size is representable as `std::streamsize`. This exercise covers bounded binary-style input and transferred-count validation.

# Solution

```cpp
auto count = static_cast<std::streamsize>(destination.size());
input.read(reinterpret_cast<char*>(destination.data()), count);
return input.gcount() == count;
```
