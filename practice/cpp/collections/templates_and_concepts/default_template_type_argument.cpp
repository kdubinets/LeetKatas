#include <string>
#include <type_traits>

template <class T>
struct Box {
    T value;
};

// Finish: define PreferredBox so omitting its type argument selects an owning string

static_assert(std::is_same_v<PreferredBox<>, Box<std::string>>);
static_assert(std::is_same_v<PreferredBox<int>, Box<int>>);
