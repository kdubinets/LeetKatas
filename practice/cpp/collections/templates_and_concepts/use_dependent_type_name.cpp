#include <string>
#include <type_traits>
#include <vector>

template <class Container>
using element_type_t =
    // Finish: select the container's nested value_type as a type

static_assert(std::is_same_v<element_type_t<std::vector<int>>, int>);
static_assert(std::is_same_v<element_type_t<std::string>, char>);
