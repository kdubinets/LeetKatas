#include <functional>

struct Counter {
    int value;

    int add(int amount) {
        value += amount;
        return value;
    }
};

int solve(Counter& counter, int (Counter::*operation)(int), int amount) {
    // Finish: call the selected operation on counter with amount and return its result
}
