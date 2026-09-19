# Name

Smallest Digits after Exact Removal

# Description

Remove exactly the requested number of digits while retaining relative order, then return the smallest resulting nonnegative decimal representation. Input is nonempty decimal digits and the count is valid. Omit leading zeroes; return "0" if nothing nonzero remains.

The supplied increasing digit stack removes larger trailing digits while budget remains, then spends any leftover budget on the suffix.

This exercise covers bounded greedy popping followed by monotonic-stack finalization.

# Solution

```cpp
std::string kept;
kept.reserve(digits.size());
for (char digit : digits) {
    while (remove_count > 0 && !kept.empty() && kept.back() > digit) {
        kept.pop_back();
        --remove_count;
    }
    kept.push_back(digit);
}
kept.resize(kept.size() - remove_count);
const std::size_t first = kept.find_first_not_of('0');
return first == std::string::npos ? "0" : kept.substr(first);
```
