#include <type_traits>

struct Value {
    double amount;

    template <class T>
    // Finish: allow implicit construction only when the source type is int
};

static_assert(std::is_convertible_v<int, Value>);
static_assert(!std::is_convertible_v<double, Value>);
static_assert(std::is_constructible_v<Value, double>);
