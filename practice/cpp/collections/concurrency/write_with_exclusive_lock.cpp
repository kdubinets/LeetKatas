#include <mutex>
#include <shared_mutex>

void write_value(int& value, std::shared_mutex& mutex, int replacement) {
    // Finish: replace the value while holding exclusive ownership of the mutex
}
