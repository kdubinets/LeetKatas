#include <concepts>
#include <string>
#include <string_view>

struct NamedValue {
    std::string name() const;
};

struct NumericValue {
    int name() const;
};

template <class T>
// Finish: require a const value's name result to be usable as a string view

static_assert(StringNamed<NamedValue>);
static_assert(!StringNamed<NumericValue>);
