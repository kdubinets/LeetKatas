#include <algorithm>
#include <array>

constexpr std::array<int, 5> sorted(std::array<int, 5> values) {
    // Finish: return the values in ascending order during constant evaluation
}

static_assert(sorted({4, 1, 5, 2, 3}) == std::array{1, 2, 3, 4, 5});
