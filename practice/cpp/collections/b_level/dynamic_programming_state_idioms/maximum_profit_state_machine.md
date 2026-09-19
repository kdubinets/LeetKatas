# Name

Maximum Trading Profit with Coupled States

# Description

Return the greatest profit from chronological buy-then-sell transactions while holding at most one item and paying the nonnegative fee on each sale. Prices are nonnegative. Empty input returns zero; do not modify prices. Arithmetic fits in long long.

The supplied two-state recurrence derives both cash and holding states from the same prior snapshot.

This exercise covers snapshot-based updates of coupled dynamic-programming states.

# Solution

```cpp
if (prices.empty()) {
    return 0;
}
long long cash = 0;
long long holding = -static_cast<long long>(prices.front());
for (std::size_t day = 1; day < prices.size(); ++day) {
    const long long old_cash = cash;
    const long long old_holding = holding;
    cash = std::max(old_cash, old_holding + prices[day] - transaction_fee);
    holding = std::max(old_holding, old_cash - prices[day]);
}
return cash;
```
