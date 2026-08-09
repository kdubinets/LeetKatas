#include <type_traits>

constexpr auto positive = [](int value) { return value > 0; };

constexpr auto solve() {
    // Finish: create a fresh object of the predicate's closure type without copying the existing object
}

static_assert(std::is_same_v<decltype(solve()), std::remove_cv_t<decltype(positive)>>);
static_assert(solve()(1));
