#include <algorithm>
#include <cstddef>
#include <optional>
#include <vector>

using namespace std;

std::optional<std::size_t> minimum_coin_count(const std::vector<std::size_t>& coins, std::size_t target) {
    // Pattern: amount-indexed minimization. Use target plus one as an unreachable sentinel and zero coins for amount zero; for each later amount consider every coin whose predecessor amount is reachable before adding one.

    // Finish: return the fewest coins needed to total target when each distinct positive coin value may be used any number of times; return 0 for target 0 and an empty optional when target is impossible; do not modify coins, and assume target plus one and every coin count fit in size_t
}
