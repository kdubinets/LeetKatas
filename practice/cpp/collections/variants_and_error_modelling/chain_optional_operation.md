# Name

Chain an Optional-Producing Operation

# Description

Given optional text and a declared parser that also returns an optional, invoke the parser only for present input and return a flat optional result. This trains C++20 optional chaining without nesting.

# Solution

```cpp
if (text) {
    return parse_port(*text);
}
return std::nullopt;
```
