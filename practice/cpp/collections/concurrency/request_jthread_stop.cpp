#include <latch>
#include <thread>

bool solve() {
    std::latch gate{1};
    bool observed = false;
    std::jthread worker([&gate, &observed](std::stop_token token) {
        gate.wait();
        observed = token.stop_requested();
    });
    // Finish: request cancellation, let the worker inspect it, wait for completion, and return what it observed
}
