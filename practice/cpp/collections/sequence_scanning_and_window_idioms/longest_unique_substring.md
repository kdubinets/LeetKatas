# Name

Longest Unique Substring

# Description

Use a shrink-to-valid sliding window to return the greatest length of a substring of `text` with no repeated byte. The invariant is that every byte frequency in the current window is at most one; shrink from the left whenever adding the right byte violates it.

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
