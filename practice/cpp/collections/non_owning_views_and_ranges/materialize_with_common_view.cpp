#include <cstddef>
#include <ranges>
#include <vector>

std::vector<int> solve(int first, std::size_t count) {
    auto values = std::views::iota(first) | std::views::take(count);
    // Finish: return all generated values in a vector in the same order
}
