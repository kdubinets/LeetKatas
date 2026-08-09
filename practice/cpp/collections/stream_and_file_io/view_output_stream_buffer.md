# Name

View an Output Stream Buffer

# Description

Return a read-only `std::string_view` over the characters currently accumulated by a caller-owned `std::ostringstream`, without copying or transferring its buffer. The caller consumes the view before modifying or destroying the stream. This exercise covers the C++20 non-owning string-stream buffer view and its lifetime boundary.

# Solution

```cpp
return output.view();
```
