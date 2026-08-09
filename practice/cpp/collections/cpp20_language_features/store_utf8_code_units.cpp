#include <string_view>
#include <type_traits>

constexpr auto solve() {
    // Finish: return a non-owning sequence of the UTF-8 code units in the given literal
}

static_assert(std::is_same_v<decltype(solve()), std::u8string_view>);
static_assert(solve() == u8"café");
