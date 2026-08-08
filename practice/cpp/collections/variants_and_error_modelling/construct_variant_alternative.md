# Name

Construct a Selected Variant Alternative

# Description

Construct a `Value` whose `std::string` alternative contains the supplied string. The explicit alternative choice should remain unambiguous if the variant's other alternatives change.

# Solution

```cpp
return Value{std::in_place_type<std::string>, std::move(text)};
```
