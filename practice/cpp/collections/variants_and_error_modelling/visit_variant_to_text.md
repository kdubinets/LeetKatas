# Name

Visit a Variant to Produce Text

# Description

Return a common string result from a const integer-or-string variant: preserve stored text and convert an integer to decimal text. This trains a generic visitor with type-specific compile-time branching.

# Solution

```cpp
return std::visit([](const auto& item) -> std::string {
    using T = std::decay_t<decltype(item)>;
    if constexpr (std::is_same_v<T, int>) {
        return std::to_string(item);
    } else {
        return item;
    }
}, value);
```
