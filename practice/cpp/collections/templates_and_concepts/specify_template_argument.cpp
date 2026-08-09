#include <type_traits>

template <class Result, class Value>
Result convert(Value value) {
    return static_cast<Result>(value);
}

double solve(int value) {
    // Finish: convert the value with double selected as the result type
}

static_assert(std::is_same_v<decltype(solve(3)), double>);
