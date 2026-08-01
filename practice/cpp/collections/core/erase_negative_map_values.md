# Name

Erase Negative Map Values

# Description

Mutate a `std::map<int, int>` by removing all entries with negative mapped values while retaining every other entry. This exercise covers safe associative-container erasure during iteration.

# Solution

```cpp
for (auto it = values.begin(); it != values.end();) {
    if (it->second < 0) {
        it = values.erase(it);
    } else {
        ++it;
    }
}
```
