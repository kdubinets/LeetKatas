# Name

Find a Comparator-Equivalent Set Value

# Description

Find a value in a const set ordered by magnitude. Return the actual stored integer whose magnitude is equivalent to the target, or no value. Inputs exclude the minimum `int` value.

# Solution

```cpp
const auto it = values.find(target);
if (it == values.end()) {
    return std::nullopt;
}
return *it;
```
