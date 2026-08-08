# Name

Chain a Result-Producing Operation

# Description

Given a string-or-error result, call the declared text measurement only for a successful string. The measurement can itself fail, so return its flat size-or-error result directly and propagate an existing input error unchanged.

# Solution

```cpp
if (const auto* value = std::get_if<std::string>(&result)) {
    return measure_text(*value);
}
return std::get<Error>(result);
```
