# Name

Extract a Word and Count

# Description

Read a whitespace-delimited `std::string` followed by an `int` from a `std::string_view`. Return both fields as a pair when extraction succeeds, or an empty optional if either field is missing or malformed. Additional trailing input may remain. This exercise covers typed sequential extraction with `std::istringstream`.

# Solution

```cpp
std::istringstream input{std::string{text}};
std::string word;
int count;
if (input >> word >> count) {
    return std::pair{std::move(word), count};
}
return std::nullopt;
```
