#include <type_traits>

template <class Expected, class... Types>
inline constexpr bool all_same_as =
    // Finish: report whether every packed type is Expected

static_assert(all_same_as<int>);
static_assert(all_same_as<int, int, int>);
static_assert(!all_same_as<int, int, long>);
