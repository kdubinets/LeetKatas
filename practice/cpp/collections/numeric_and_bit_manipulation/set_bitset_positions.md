# Name

Set Listed Bitset Positions

# Description

Build and return a `std::bitset<64>` with every zero-based position listed in a const vector set to one and all other positions zero. Positions may repeat, and the caller guarantees they are below 64. This exercise covers indexed mutation of a fixed-size standard bitset.

# Solution

```cpp
std::bitset<64> result;
for (auto position : positions) {
    result.set(position);
}
return result;
```
