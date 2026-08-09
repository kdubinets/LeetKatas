# Name

Longest Substring With a Distinct-Byte Limit

# Description

Use a shrink-to-valid sliding window to return the greatest length of a substring of `text` containing at most `limit` distinct bytes. `limit` may be zero. Maintain byte counts for exactly the current window and remove a key when its count reaches zero.

# Solution

```cpp
if (limit == 0) {
    return 0;
}

std::unordered_map<unsigned char, int> counts;
std::size_t left = 0;
std::size_t best = 0;
for (std::size_t right = 0; right < text.size(); ++right) {
    ++counts[static_cast<unsigned char>(text[right])];
    while (counts.size() > limit) {
        const auto leaving = static_cast<unsigned char>(text[left]);
        if (--counts[leaving] == 0) {
            counts.erase(leaving);
        }
        ++left;
    }
    best = std::max(best, right - left + 1);
}
return best;
```
