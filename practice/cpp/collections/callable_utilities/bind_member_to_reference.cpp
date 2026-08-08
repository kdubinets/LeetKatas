#include <functional>

struct Accumulator {
    int total = 0;

    int add(int value) {
        total += value;
        return total;
    }
};

std::function<int(int)> solve(Accumulator& accumulator) {
    // Finish: return a unary callable that updates this existing accumulator
}
