#include <exception>
#include <future>

void run_and_report(std::promise<int>& result, int (*work)()) {
    try {
        result.set_value(work());
    } catch (...) {
        // Finish: preserve the active failure in the promise so its future rethrows it
    }
}
