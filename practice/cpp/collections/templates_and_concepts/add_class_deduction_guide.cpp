#include <string>
#include <type_traits>

using namespace std;

template <class T>
struct Holder {
    T value;
};

// Finish: make construction from a C string select an owning string as the stored type

Holder value{"hello"};
static_assert(std::is_same_v<decltype(value), Holder<std::string>>);
