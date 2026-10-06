# Name

Running Medians from Two Balanced Heaps

# Description

Return one median per input element in prefix order. The median is the middle value of a sorted odd-length prefix, or the arithmetic mean of the two middle values of a sorted even-length prefix. Empty input returns empty. Preserve values and avoid integer overflow when averaging.

Use two initially empty heaps for lower and upper halves. Every lower-half value is at most every upper-half value, and the lower half has the same size or one extra value. Maintain both invariants after every insertion; the heap boundaries determine the median.

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
