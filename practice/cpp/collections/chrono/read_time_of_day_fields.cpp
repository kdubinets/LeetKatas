#include <chrono>
#include <tuple>

using TimeFields = std::tuple<
    std::chrono::hours,
    std::chrono::minutes,
    std::chrono::seconds,
    std::chrono::milliseconds>;

TimeFields solve(
    const std::chrono::hh_mm_ss<std::chrono::milliseconds>& value) {
    // Finish: return the hour, minute, second, and subsecond fields
}
