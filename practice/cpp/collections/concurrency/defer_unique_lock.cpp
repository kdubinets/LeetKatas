#include <mutex>

void increment_after_preparation(int& value, std::mutex& mutex) {
    // Finish: create lock ownership without acquiring the mutex, then acquire it before mutating the value
}
