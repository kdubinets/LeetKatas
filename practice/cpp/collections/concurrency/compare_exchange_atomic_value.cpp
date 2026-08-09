#include <atomic>

bool replace_if_observed(std::atomic<int>& value,
                         int& expected,
                         int desired) {
    // Finish: replace the atomic value only if it matches the caller's expectation and update that expectation on failure
}
