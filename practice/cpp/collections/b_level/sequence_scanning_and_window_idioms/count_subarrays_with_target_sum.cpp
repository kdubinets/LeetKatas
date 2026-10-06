#include <cstddef>
#include <unordered_map>
#include <vector>

using namespace std;

std::size_t count_subarrays_with_target_sum(const std::vector<int>& values, long long target) {
    // Pattern: prefix-frequency scan. Initially record one empty prefix with sum zero; count earlier prefixes differing from the current prefix by target before recording the current prefix.

    // Finish: return the number of nonempty contiguous ranges whose sum equals target, counting overlapping ranges separately; negative values are allowed and empty input returns zero; preserve values, all prefix sums and their differences from target fit in long long, and the result fits in size_t
}
