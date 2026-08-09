#include <concepts>
#include <string_view>

template <class T>
concept Number = std::integral<T> || std::floating_point<T>;

template <class T>
concept WholeNumber = Number<T> && std::integral<T>;

template <Number T>
constexpr std::string_view category(T) {
    return "number";
}

// Finish: add the refined overload that identifies whole numbers

static_assert(category(1) == "whole");
static_assert(category(1.5) == "number");
