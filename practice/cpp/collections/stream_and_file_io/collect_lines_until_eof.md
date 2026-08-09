# Name

Collect Lines Until EOF

# Description

Read every remaining complete line from a caller-provided `std::istream&` into a vector, preserving order and empty lines. Return the vector when iteration ends at normal end-of-file, including for empty input; return an empty optional when another stream failure stops reading. This exercise covers the conventional line-reading loop and post-loop stream-state classification.

# Solution

```cpp
std::vector<std::string> lines;
std::string line;
while (std::getline(input, line)) {
    lines.push_back(std::move(line));
}
if (!input.eof() || input.bad()) {
    return std::nullopt;
}
return lines;
```
