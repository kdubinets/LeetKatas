#include <chrono>

using MillisecondSystemTime = std::chrono::time_point<
    std::chrono::system_clock,
    std::chrono::milliseconds>;

MillisecondSystemTime solve(std::chrono::system_clock::time_point value) {
    // Finish: truncate the time point to millisecond precision
}
