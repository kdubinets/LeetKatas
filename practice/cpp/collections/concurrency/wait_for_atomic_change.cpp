#include <atomic>

int wait_for_change(std::atomic<int>& state, int observed) {
    // Finish: block while the state equals the observed value, then return its new value
}
