#include <mutex>
#include <shared_mutex>

int read_value(const int& value, std::shared_mutex& mutex) {
    // Finish: return the protected value while still allowing other readers to proceed concurrently
}
