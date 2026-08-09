#include <array>
#include <cstddef>

constexpr std::array<int, 6> make_squares() {
    // Finish: build and return a table whose element at each index is that index squared
}

constexpr auto squares = make_squares();
static_assert(squares[0] == 0);
static_assert(squares[3] == 9);
static_assert(squares[5] == 25);
