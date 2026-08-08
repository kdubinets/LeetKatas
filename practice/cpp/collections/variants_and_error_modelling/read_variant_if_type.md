# Name

Read a Variant Alternative Safely

# Description

Copy the text from a const integer-or-string variant when that alternative is active; otherwise return an empty optional. The operation must not throw for the integer state.

# Solution

```cpp
if (const auto* text = std::get_if<std::string>(&value)) {
    return *text;
}
return std::nullopt;
```
