#include <algorithm>
#include <array>

constexpr std::array<int, 4> squared(const std::array<int, 4>& values) {
    std::array<int, 4> result{};
    // Finish: fill the result with squared input values during constant evaluation and return it
}

static_assert(squared({1, 2, 3, 4}) == std::array{1, 4, 9, 16});
