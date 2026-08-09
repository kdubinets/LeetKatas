#include <string>
#include <type_traits>

template <class T>
struct storage_type {
    using type = T;
};

// Finish: map const char* to an owning string while leaving the primary mapping unchanged

static_assert(std::is_same_v<storage_type<const char*>::type, std::string>);
static_assert(std::is_same_v<storage_type<int>::type, int>);
