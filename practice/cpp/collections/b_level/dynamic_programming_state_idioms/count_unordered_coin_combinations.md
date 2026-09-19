# Name

Count Unordered Coin Combinations

# Description

Return the number of combinations totaling target when each coin value may be used any number of times. Coin values are positive and distinct. Order does not distinguish combinations, so using 2 then 3 is the same combination as using 3 then 2. Target zero has one empty combination. Do not modify coins. All counts fit in long long.

The supplied dynamic-programming transition uses one amount row initialized with one way to form zero. Coins are processed outside, and amounts increase from the current coin so that coin remains reusable without counting permutations.

This exercise covers ascending in-place amount updates for reusable choices.

# Solution

```cpp
std::vector<long long> ways(target + 1, 0);
ways[0] = 1;
for (std::size_t coin : coins) {
    if (coin > target) {
        continue;
    }
    for (std::size_t amount = coin; amount <= target; ++amount) {
        ways[amount] += ways[amount - coin];
    }
}
return ways[target];
```
