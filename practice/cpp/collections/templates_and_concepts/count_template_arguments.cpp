#include <cstddef>

template <class... Types>
constexpr std::size_t type_count() {
    // Finish: return how many types were supplied
}

static_assert(type_count<>() == 0);
static_assert(type_count<int, double, char>() == 3);
