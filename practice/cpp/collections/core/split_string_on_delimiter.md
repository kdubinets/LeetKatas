# Name

Split String on Delimiter

# Description

Split a const `std::string` at every occurrence of a delimiter character and return all parts in order. Preserve empty parts between adjacent delimiters and at either end; an empty input produces one empty part. This exercise covers repeated string search and substring extraction.

# Solution

```cpp
std::size_t start = 0;
std::size_t position = text.find(delimiter, start);
while (position != std::string::npos) {
    parts.push_back(text.substr(start, position - start));
    start = position + 1;
    position = text.find(delimiter, start);
}
parts.push_back(text.substr(start));
```
