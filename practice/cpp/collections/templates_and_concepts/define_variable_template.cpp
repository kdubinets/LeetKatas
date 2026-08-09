#include <type_traits>

// Finish: define a Boolean variable template that reports whether T is a pointer

static_assert(is_pointer_type<int*>);
static_assert(!is_pointer_type<int>);
