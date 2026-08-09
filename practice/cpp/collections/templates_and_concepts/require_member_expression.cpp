#include <string>
#include <vector>

template <class T>
// Finish: define HasClear for types whose mutable value supports a zero-argument clear operation

static_assert(HasClear<std::string>);
static_assert(HasClear<std::vector<int>>);
static_assert(!HasClear<int>);
