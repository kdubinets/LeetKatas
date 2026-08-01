# Name

Deduplicate While Preserving Order

# Description

Return a new integer vector containing only the first occurrence of each value from a const input vector, preserving original order. The input may be unsorted and must remain unchanged. This exercise covers combining uniqueness tracking with stable output construction.

# Solution

```cpp
for (int value : values) {
    if (seen.insert(value).second) {
        result.push_back(value);
    }
}
```
