#include <concepts>
#include <type_traits>
#include <utility>

template <class Left, class Right>
// Finish: define add only when both arguments have the same normalized type

int main() {
    int left = 2;
    const int right = 3;
    return add(left, right) == 5 ? 0 : 1;
}
