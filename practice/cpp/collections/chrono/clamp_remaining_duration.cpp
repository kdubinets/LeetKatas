#include <chrono>

using MillisecondPoint = std::chrono::time_point<
    std::chrono::steady_clock,
    std::chrono::milliseconds>;

std::chrono::milliseconds solve(
    MillisecondPoint now,
    MillisecondPoint deadline) {
    // Finish: return the nonnegative time remaining until the deadline
}
