# Name

Longest Unique Substring

# Description

Return the length of the longest contiguous substring of `text` in which every byte occurs at most once. Empty text produces zero. The task concerns bytes, rather than decoded Unicode characters.

The supplied pattern is a shrink-to-valid sliding window whose byte frequencies are all at most one when its length is considered.

This exercise covers restoring byte uniqueness by shrinking a sliding window after a repeated byte enters.

# Solution

```cpp
std::array<int, 256> frequencies{};
std::size_t left = 0;
std::size_t best = 0;
for (std::size_t right = 0; right < text.size(); ++right) {
    const auto entering = static_cast<unsigned char>(text[right]);
    ++frequencies[entering];
    while (frequencies[entering] > 1) {
        --frequencies[static_cast<unsigned char>(text[left])];
        ++left;
    }
    best = std::max(best, right - left + 1);
}
return best;
```
