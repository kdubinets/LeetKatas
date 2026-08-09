#include <thread>

int solve() {
    int result = 0;
    std::thread worker([&result] { result = 42; });
    // Finish: wait for the worker to finish before returning the value it produced
}
