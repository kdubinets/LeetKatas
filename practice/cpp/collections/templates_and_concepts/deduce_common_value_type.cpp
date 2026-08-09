#include <type_traits>

template <class... Types>
using common_value_t =
    // Finish: select the type all supplied types can commonly convert to

static_assert(std::is_same_v<common_value_t<int, double>, double>);
static_assert(std::is_same_v<common_value_t<char, short, int>, int>);
