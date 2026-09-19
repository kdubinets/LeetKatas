# Name

Longest Substring With a Distinct-Byte Limit

# Description

Return the length of the longest contiguous substring of `text` containing at most `limit` different byte values. Return zero when the text is empty or the limit is zero. The task concerns bytes, rather than decoded Unicode characters.

The supplied pattern is a shrink-to-valid sliding window whose frequency state represents the current substring and whose distinct-byte count does not exceed the limit when its length is considered.

This exercise covers restoring a distinct-byte limit by shrinking a frequency window and removing exhausted keys.

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
