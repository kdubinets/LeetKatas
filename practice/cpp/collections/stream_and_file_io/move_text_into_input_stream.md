# Name

Move Text into an Input Stream

# Description

Construct a `std::istringstream`, transfer the by-value `std::string` into its underlying buffer, and return the stream ready for reading. This exercise covers the C++20 rvalue string-buffer setter that avoids an unnecessary copy of owned text.

# Solution

```cpp
std::istringstream input;
input.str(std::move(text));
return input;
```
