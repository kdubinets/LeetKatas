# Name

Write a Synchronized Record

# Description

Write `label=value` followed by a newline to the supplied stream so the complete record is emitted without interleaving with records concurrently written through other synchronized stream wrappers. This trains C++20 `std::osyncstream` buffering and scope-based emission.

# Solution

```cpp
std::osyncstream synchronized(output);
synchronized << label << '=' << value << '\n';
```
