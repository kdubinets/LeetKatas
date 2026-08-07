# Name

Split Text on Regular-Expression Matches

# Description

Use a precompiled `std::regex` as a separator and return the unmatched portions of a const `std::string` in encounter order. Preserve the empty fields that the standard token iterator reports, and return the complete input as one field when there is no match. This exercise covers selecting unmatched subsequences with `std::sregex_token_iterator`; it does not test separator syntax.

# Solution

```cpp
std::vector<std::string> fields;
for (std::sregex_token_iterator it{text.begin(), text.end(), separator, -1}, end;
     it != end;
     ++it) {
    fields.push_back(it->str());
}
return fields;
```
