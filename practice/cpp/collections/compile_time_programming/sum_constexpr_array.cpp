#include <array>

constexpr int sum(const std::array<int, 4>& values) {
    // Finish: return the total in a form that can be evaluated at compile time
}

static_assert(sum({2, 3, 5, 7}) == 17);
