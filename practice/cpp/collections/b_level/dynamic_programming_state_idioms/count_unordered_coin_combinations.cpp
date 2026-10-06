#include <cstddef>
#include <vector>

using namespace std;

long long count_coin_combinations(
    const std::vector<std::size_t>& coins,
    std::size_t target) {
    // Pattern: one amount row for reusable choices, initially zero except one way to form amount zero. Process each coin outside and amounts from that coin upward; add the ways at amount minus coin to the current amount.

    // Finish: return the number of combinations totaling target using the distinct positive coin values any number of times, with selection order ignored; target zero has one empty combination, and an impossible target returns zero; preserve coins, target plus one fits in size_t, and all counts fit in long long
}
