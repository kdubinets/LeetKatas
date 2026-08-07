# Name

Split String View Fields

# Description

Split a `std::string_view` at each delimiter and return the resulting fields as string views into the original characters. Preserve empty fields produced by adjacent or boundary delimiters, while an empty input produces no fields. This exercise covers converting split-view subranges into non-owning string slices.

# Solution

```cpp
for (auto field : text | std::views::split(delimiter)) {
    result.emplace_back(
        field.begin(),
        static_cast<std::size_t>(std::ranges::distance(field)));
}
```
