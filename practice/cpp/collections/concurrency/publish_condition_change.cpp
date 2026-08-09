#include <condition_variable>
#include <mutex>

void mark_ready(bool& ready,
                std::mutex& mutex,
                std::condition_variable& changed) {
    // Finish: publish readiness while protected, then wake one waiter after releasing the mutex
}
