#include <cstddef>
#include <unordered_map>
#include <vector>

std::size_t count_subarrays_with_target_sum(const std::vector<int>& values, long long target) {
    // Pattern: prefix-frequency scan. Count earlier prefixes that differ from the current prefix by target before recording the current prefix.
    // Finish: return the number of contiguous subarrays whose sum equals target
}
