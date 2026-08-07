# Name

Append Formatted Text

# Description

Append a `std::string_view` label, an equals sign, and an `int` directly to a mutable `std::string`, preserving its existing contents. This exercise covers formatted output through an output iterator without constructing an intermediate formatted string.

# Solution

```cpp
std::format_to(std::back_inserter(output), "{}={}", label, value);
```
