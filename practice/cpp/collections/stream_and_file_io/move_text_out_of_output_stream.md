# Name

Move Text out of an Output Stream

# Description

Extract and return the accumulated text from the by-value `std::ostringstream` by transferring its buffer into the result. This exercise covers the C++20 rvalue-qualified string-buffer getter rather than copying from an lvalue stream.

# Solution

```cpp
return std::move(output).str();
```
