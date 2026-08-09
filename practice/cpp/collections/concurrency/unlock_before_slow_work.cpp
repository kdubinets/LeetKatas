#include <mutex>

void consume_snapshot(const int& value,
                      std::mutex& mutex,
                      void (*work)(int) noexcept) {
    // Finish: copy the protected value and release its mutex before passing the copy to the supplied work
}
