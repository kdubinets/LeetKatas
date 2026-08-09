#include <type_traits>

template <class T>
struct is_raw_pointer : std::false_type {};

// Finish: make the trait true for every raw pointer type

static_assert(is_raw_pointer<int*>::value);
static_assert(is_raw_pointer<const double*>::value);
static_assert(!is_raw_pointer<int>::value);
