# Name

Drain Priority Queue Descending

# Description

Consume a by-value copy of a max-priority `std::priority_queue<int>` and return all its elements from greatest to smallest. The caller's original queue is preserved by the intentional parameter copy. This exercise covers repeated heap-top access and removal.

# Solution

```cpp
while (!values.empty()) {
    result.push_back(values.top());
    values.pop();
}
```
