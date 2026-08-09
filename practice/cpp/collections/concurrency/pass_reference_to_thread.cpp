#include <functional>
#include <thread>

void increment(int& value) {
    ++value;
}

void solve(int& value) {
    // Finish: run the increment operation on a worker without copying the caller's integer, then wait for completion
}
