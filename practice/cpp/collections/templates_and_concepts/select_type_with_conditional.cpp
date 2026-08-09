#include <type_traits>

template <bool UseFirst, class First, class Second>
// Finish: define selected_t as First when the condition holds and Second otherwise

static_assert(std::is_same_v<selected_t<true, int, double>, int>);
static_assert(std::is_same_v<selected_t<false, int, double>, double>);
