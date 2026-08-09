#include <condition_variable>
#include <mutex>
#include <stop_token>

bool wait_until_ready(std::condition_variable_any& changed,
                      std::mutex& mutex,
                      std::stop_token token,
                      const bool& ready) {
    // Finish: wait for readiness or cancellation and report whether readiness won
}
