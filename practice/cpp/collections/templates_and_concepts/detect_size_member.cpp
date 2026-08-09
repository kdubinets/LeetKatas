#include <string>
#include <type_traits>
#include <utility>

template <class T, class = void>
struct has_size_member : std::false_type {};

// Finish: make the trait true when calling size on a const T is well-formed

static_assert(has_size_member<std::string>::value);
static_assert(!has_size_member<int>::value);
