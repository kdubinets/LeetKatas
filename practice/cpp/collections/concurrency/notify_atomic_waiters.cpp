#include <atomic>

void publish_state(std::atomic<int>& state, int value) {
    // Finish: store the new state and wake every thread waiting on this atomic object
}
