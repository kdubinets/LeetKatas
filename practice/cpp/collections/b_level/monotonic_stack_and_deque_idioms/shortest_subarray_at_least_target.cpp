#include <algorithm>
#include <cstddef>
#include <deque>
#include <optional>
#include <vector>

using namespace std;

std::optional<std::size_t> shortest_subarray_at_least_target(const std::vector<int>& values, long long target) {
    // Pattern: increasing deque of prefix-sum indices. For each prefix, remove front indices while their difference reaches target, updating the shortest length; then remove back indices whose prefix sums are no smaller than the current prefix.

    // Finish: return the length of the shortest nonempty contiguous range whose sum is at least target, or an empty optional if none exists; values may contain negative numbers, target is positive, no input sum overflows long long, and values is not modified
}
