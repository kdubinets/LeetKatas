#include <utility>

template <class Function, class... Args>
void for_each_argument(Function&& function, Args&&... args) {
    // Finish: call the function once for every argument from left to right
}

int main() {
    int total = 0;
    for_each_argument([&total](int value) { total = total * 10 + value; }, 1, 2, 3);
    return total == 123 ? 0 : 1;
}
