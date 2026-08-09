#include <vector>

template <class T>
// Finish: define HasValueType for types that declare a nested value_type

static_assert(HasValueType<std::vector<int>>);
static_assert(!HasValueType<int>);
