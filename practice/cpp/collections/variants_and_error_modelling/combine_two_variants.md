# Name

Visit Two Variants Together

# Description

Visit two const integer-or-string variants simultaneously and join their text forms with a colon. Strings remain unchanged and integers use decimal conversion.

# Solution

```cpp
auto text = [](const auto& item) {
    using T = std::decay_t<decltype(item)>;
    if constexpr (std::is_same_v<T, int>) return std::to_string(item);
    else return item;
};
return std::visit([&](const auto& a, const auto& b) {
    return text(a) + ":" + text(b);
}, left, right);
```
