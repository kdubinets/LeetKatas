#include <condition_variable>
#include <mutex>

using namespace std;

void wait_until_ready(std::condition_variable& changed,
                      std::mutex& mutex,
                      const bool& ready) {
    // Finish: wait while holding the mutex until the supplied state reports readiness
}
