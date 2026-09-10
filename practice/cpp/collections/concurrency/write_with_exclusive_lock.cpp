#include <mutex>
#include <shared_mutex>

using namespace std;

void write_value(int& value, std::shared_mutex& mutex, int replacement) {
    // Finish: replace the value while holding exclusive ownership of the mutex
}
