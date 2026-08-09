# Name

Read a Count and the Next Line

# Description

Read an `int` from a caller-provided `std::istream&`, discard the remainder of that integer's line, and then read the following complete line. Return both values as a pair, or an empty optional if either read fails. This exercise covers a deliberate transition from formatted extraction to line-oriented input without returning the leftover newline as an empty record.

# Solution

```cpp
int count;
if (!(input >> count)) {
    return std::nullopt;
}
input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
std::string line;
if (!std::getline(input, line)) {
    return std::nullopt;
}
return std::pair{count, std::move(line)};
```
