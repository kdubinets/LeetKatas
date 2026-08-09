#include <atomic>

void publish(int& payload, std::atomic<bool>& ready, int value) {
    // Finish: write the payload and then make its availability safely observable by a matching consumer
}
