#include <type_traits>

template <class T>
// Finish: define normalized_t as T without reference or cv qualification

static_assert(std::is_same_v<normalized_t<const int&>, int>);
static_assert(std::is_same_v<normalized_t<volatile double&&>, double>);
