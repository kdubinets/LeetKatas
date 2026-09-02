# Name

Count Fixed-Window Anagram Matches

# Description

Use a fixed-size character-frequency window to count substrings of `text` that are anagrams of `pattern`. Both strings contain lowercase English letters; an empty `pattern` has zero matches. Keep the window frequency state equal to the current substring while it slides.

# Solution

```cpp
std::array<int, 26> needed{};
std::array<int, 26> window{};
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
