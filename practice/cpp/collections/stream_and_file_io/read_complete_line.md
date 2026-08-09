# Name

Read a Complete Line

# Description

Read the next complete line from a caller-provided `std::istream&`, excluding the line delimiter. Return the line, including when it is empty, or an empty optional if no line can be read. This exercise covers line-oriented unformatted input without taking ownership of the stream.

# Solution

```cpp
std::string line;
if (std::getline(input, line)) {
    return line;
}
return std::nullopt;
```
