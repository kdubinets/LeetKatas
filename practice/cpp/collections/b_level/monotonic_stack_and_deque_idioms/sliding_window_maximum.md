# Name

Maximum of Every Fixed Window

# Description

Return each exact-width contiguous window maximum from left to right. Input is nonempty and width is valid. Preserve values.

The supplied decreasing deque holds candidate indices, expiring old indices at the front and removing dominated values at the back.

This exercise covers simultaneous expiration and dominance maintenance in a monotonic deque.

# Solution

```cpp
std::vector<int> result;
result.reserve(values.size() - width + 1);
std::deque<std::size_t> candidates;
for (std::size_t index = 0; index < values.size(); ++index) {
    while (!candidates.empty() && candidates.front() + width <= index) {
        candidates.pop_front();
    }
    while (!candidates.empty() &&
           values[candidates.back()] <= values[index]) {
        candidates.pop_back();
    }
    candidates.push_back(index);
    if (index + 1 >= width) {
        result.push_back(values[candidates.front()]);
    }
}
return result;
```
