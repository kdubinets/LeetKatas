# Name

Inclusive Previous-Greater Spans

# Description

For each position, return the longest contiguous range ending there in which every value is no greater than the ending value. Preserve prices; empty input produces an empty result.

The supplied decreasing index stack exposes the previous strictly greater boundary after removing lesser or equal prices.

This exercise covers conversion of a previous-greater boundary into an inclusive span.

# Solution

```cpp
std::vector<std::size_t> spans(prices.size());
std::vector<std::size_t> greater;
for (std::size_t index = 0; index < prices.size(); ++index) {
    while (!greater.empty() && prices[greater.back()] <= prices[index]) {
        greater.pop_back();
    }
    spans[index] = greater.empty() ? index + 1 : index - greater.back();
    greater.push_back(index);
}
return spans;
```
