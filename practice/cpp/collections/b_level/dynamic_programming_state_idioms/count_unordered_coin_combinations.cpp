#include <cstddef>
#include <vector>

using namespace std;

long long count_coin_combinations(
    const std::vector<std::size_t>& coins,
    std::size_t target) {
    // Pattern: one amount row for reusable choices. Set ways[0] to one, process each coin outside, and visit amounts from that coin upward so ways[amount] += ways[amount - coin].

    // Finish: return the number of combinations totaling target when each distinct positive coin value may be used any number of times and order does not distinguish combinations; return 1 when target is 0; do not modify coins, and assume every count fits in long long
}
