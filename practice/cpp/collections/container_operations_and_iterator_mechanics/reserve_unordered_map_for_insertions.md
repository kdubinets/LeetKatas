# Name

Reserve an Unordered Map for Insertions

# Description

Before bulk insertion, reserve capacity in `destination` for its current size plus every entry in `additions`, then insert that range. Existing mapped values must win when keys collide, and `additions` remains unchanged. This exercise covers pre-sizing an unordered container to avoid avoidable rehashing during a known insertion batch.

# Solution

```cpp
destination.reserve(destination.size() + additions.size());
destination.insert(additions.begin(), additions.end());
```
