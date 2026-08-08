# Name

Transform a Successful Result Value

# Description

Map successful string data in a value-or-error variant to its length while copying any existing error unchanged. This trains explicit result transformation in C++20.

# Solution

```cpp
if (const auto* value = std::get_if<std::string>(&result)) {
    return value->size();
}
return std::get<Error>(result);
```
