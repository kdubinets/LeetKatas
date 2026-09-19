# Name

Retain the K Smallest Values

# Description

Return the smallest count values sorted nondecreasingly, preserving duplicate multiplicity. Count is valid, zero returns empty, and input is unchanged.

The supplied maximum heap is trimmed whenever it exceeds count, so it retains exactly the best bounded candidates seen.

This exercise covers bounded reversed-heap retention of globally best candidates.

# Solution

```cpp
std::priority_queue<int> retained;
for (int value : values) {
    retained.push(value);
    if (retained.size() > count) {
        retained.pop();
    }
}
std::vector<int> result(retained.size());
for (std::size_t index = result.size(); index > 0; --index) {
    result[index - 1] = retained.top();
    retained.pop();
}
return result;
```
