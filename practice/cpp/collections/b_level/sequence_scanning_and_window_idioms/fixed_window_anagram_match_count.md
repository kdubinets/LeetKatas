# Name

Count Fixed-Window Anagram Matches

# Description

Return the number of substrings of `text` of length `pattern.size()` containing exactly the same letters, with the same counts, as `pattern`. Overlapping matches count separately. Both strings contain only lowercase English letters. Return zero for an empty pattern or one longer than the text. Preserve both strings.

The supplied pattern is a fixed-size character-frequency window whose counts represent exactly the current substring.

This exercise covers maintaining a fixed-width character-frequency window and comparing it with a target frequency state.

# Solution

```cpp
if (pattern.empty() || pattern.size() > text.size()) {
    return 0;
}

std::array<std::size_t, 26> needed{};
std::array<std::size_t, 26> window{};
std::size_t matches = 0;
for (char character : pattern) {
    ++needed[static_cast<std::size_t>(character - 'a')];
}

for (std::size_t right = 0; right < text.size(); ++right) {
    ++window[static_cast<std::size_t>(text[right] - 'a')];
    if (right >= pattern.size()) {
        --window[static_cast<std::size_t>(text[right - pattern.size()] - 'a')];
    }
    if (right + 1 >= pattern.size() && window == needed) {
        ++matches;
    }
}
return matches;
```
