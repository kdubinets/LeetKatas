# Name

Branch on a Type Category

# Description

For integral `T`, return `std::to_string(value)`; otherwise return `value`, with the supported non-integral call using `std::string`. Ensure only the valid branch is instantiated for each type.

# Solution

```cpp
if constexpr (std::is_integral_v<T>) {
    return std::to_string(value);
} else {
    return value;
}
```
