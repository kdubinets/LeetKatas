#include <algorithm>
#include <vector>

using namespace std;

long long maximum_trading_profit(const std::vector<int>& prices, int transaction_fee) {
    // Pattern: two-state dynamic program: cash is the best profit while holding nothing and holding is the best profit while holding one item. Initially cash is zero and holding is minus the first price; for each later price, next cash is the greater of prior cash and prior holding plus price minus fee, and next holding is the greater of prior holding and prior cash minus price. Derive both from the same prior snapshot.

    // Finish: return the greatest realized profit from any number of chronological buy-then-sell transactions, holding at most one item and paying transaction_fee on every sale; prices and fee are nonnegative, doing nothing is allowed, and finish holding nothing; return zero for empty input, preserve prices, and all arithmetic fits in long long
}
