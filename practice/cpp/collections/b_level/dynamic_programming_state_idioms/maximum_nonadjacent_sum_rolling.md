# Name

Maximum Nonadjacent Sum with Rolling State

# Description

Return the greatest sum obtainable by selecting values at indices of which no two are adjacent. Selecting no values is allowed, so empty and all-negative inputs return zero. Do not modify the input. All intermediate and final sums fit in long long.

The supplied dynamic-programming recurrence compares the prior best result with the result two positions back plus the current value. Two rolling scalar states represent those prior results.

This exercise covers two-state rolling implementation of a supplied linear recurrence.

# Solution

```cpp
long long two_back = 0;
long long one_back = 0;
for (int value : values) {
    const long long current =
        std::max(one_back, two_back + static_cast<long long>(value));
    two_back = one_back;
    one_back = current;
}
return one_back;
```
