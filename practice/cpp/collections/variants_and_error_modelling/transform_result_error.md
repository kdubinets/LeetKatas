# Name

Transform an Explicit Result Error

# Description

Map the error state of an integer-or-error result to descriptive text through the declared helper while preserving a successful integer unchanged. The output remains an explicit success-or-error variant.

# Solution

```cpp
if (const auto* value = std::get_if<int>(&result)) {
    return *value;
}
return describe(std::get<Error>(result));
```
