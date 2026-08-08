# Name

Define Transparent Unordered Policies

# Description

Define the hash and equality policies for an unordered set of owning strings so it can also accept `std::string_view` lookup keys without allocation. Equal owning and non-owning representations must produce identical hashes.

# Solution

```cpp
struct NameHash {
    using is_transparent = void;
    std::size_t operator()(std::string_view value) const { return std::hash<std::string_view>{}(value); }
    std::size_t operator()(const std::string& value) const { return (*this)(std::string_view{value}); }
};
struct NameEqual {
    using is_transparent = void;
    bool operator()(std::string_view left, std::string_view right) const { return left == right; }
};
```
