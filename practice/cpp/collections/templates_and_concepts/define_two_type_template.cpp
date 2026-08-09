#include <utility>

// Finish: define a function that independently deduces and stores its two argument types

int main() {
    auto value = make_values(4, 2.5);
    return value.first == 4 && value.second == 2.5 ? 0 : 1;
}
