# Name

Minimum Coin Count with an Unreachable Sentinel

# Description

Return the fewest coins needed to total target using positive distinct coin values any number of times. Return zero for target zero and an empty optional if impossible. Do not modify coins. Target plus one and all counts fit in size_t.

The supplied amount-indexed recurrence uses target plus one as an unreachable sentinel and adds one only to reachable predecessor states.

This exercise covers safe minimization with an explicit unreachable-state sentinel.

# Solution

```cpp
const std::size_t unreachable = target + 1;
std::vector<std::size_t> best(target + 1, unreachable);
best[0] = 0;
for (std::size_t amount = 1; amount <= target; ++amount) {
    for (std::size_t coin : coins) {
        if (coin <= amount && best[amount - coin] != unreachable) {
            best[amount] = std::min(best[amount], best[amount - coin] + 1);
        }
    }
}
if (best[target] == unreachable) {
    return std::nullopt;
}
return best[target];
```
