# Name

Compile a Case-Insensitive Regular Expression

# Description

Compile a `std::string_view` expression into a reusable `std::regex` using ECMAScript rules with case-insensitive matching. Return an empty optional when construction reports invalid regex syntax. This exercise covers combining syntax options and translating `std::regex_error` into a value result; it does not test writing expression syntax.

# Solution

```cpp
try {
    return std::regex{
        expression.begin(),
        expression.end(),
        std::regex_constants::ECMAScript | std::regex_constants::icase};
} catch (const std::regex_error&) {
    return std::nullopt;
}
```
