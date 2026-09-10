#include <string>
#include <type_traits>
#include <vector>

using namespace std;

// Finish: define Sequence<T> as a dynamic sequence containing T values

static_assert(std::is_same_v<Sequence<std::string>, std::vector<std::string>>);
