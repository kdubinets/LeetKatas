# Name

Compare Case-Insensitive Text Weakly

# Description

Compare labels lexicographically after ASCII case folding. Spellings that differ only by letter case are equivalent rather than identical, so return an appropriate three-way comparison category.

# Solution

```cpp
const auto size = std::min(left.text.size(), right.text.size());
for (std::size_t i = 0; i < size; ++i) {
    if (const auto order = ascii_lower(left.text[i]) <=> ascii_lower(right.text[i]); order != 0) {
        return order;
    }
}
return left.text.size() <=> right.text.size();
```
