# Name

Quote Text for a Stream

# Description

Return a `std::string_view` encoded as one double-quoted stream field. Embedded double quotes and backslashes must be escaped so standard quoted extraction can recover the original text. This exercise covers `std::quoted` output.

# Solution

```cpp
std::ostringstream output;
output << std::quoted(text);
return output.str();
```
