# Name

Maximum Trading Profit with Coupled States

# Description

Return the greatest realized profit from any number of chronological buy-then-sell transactions, holding at most one item and paying transaction_fee on every sale. Prices and the fee are nonnegative. Doing nothing is allowed; finish holding nothing. Empty input returns zero. Preserve prices, and assume all arithmetic fits in long long.

Cash is the best profit while holding nothing; holding is the best profit while holding one item. Initialize them to zero and minus the first price. For each later price, next cash is the greater of prior cash and prior holding plus price minus fee; next holding is the greater of prior holding and prior cash minus price. Derive both from the same prior snapshot.

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
