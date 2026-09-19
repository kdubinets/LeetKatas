# Name

Running Medians from Two Balanced Heaps

# Description

Return the median of every nonempty prefix. Odd prefixes use the middle value and even prefixes use the mean of both middle values. Empty input returns empty; preserve values and widen even-prefix addition.

The supplied two heaps partition the lower and upper halves and maintain equal sizes or one extra value in the lower half.

This exercise covers ordering and size balancing between two streaming heaps.

# Solution

```cpp
std::priority_queue<int> lower;
std::priority_queue<int, std::vector<int>, std::greater<>> upper;
std::vector<double> medians;
medians.reserve(values.size());
for (int value : values) {
    if (lower.empty() || value <= lower.top()) {
        lower.push(value);
    } else {
        upper.push(value);
    }
    if (lower.size() > upper.size() + 1) {
        upper.push(lower.top());
        lower.pop();
    } else if (upper.size() > lower.size()) {
        lower.push(upper.top());
        upper.pop();
    }
    if (lower.size() == upper.size()) {
        medians.push_back(
            (static_cast<long long>(lower.top()) + upper.top()) / 2.0);
    } else {
        medians.push_back(lower.top());
    }
}
return medians;
```
