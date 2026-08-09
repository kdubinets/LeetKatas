#include <concepts>

template <class T>
concept Arithmetic = std::integral<T> || std::floating_point<T>;

// Finish: define square with a directly constrained template parameter

int main() {
    return square(4) == 16 && square(1.5) == 2.25 ? 0 : 1;
}
