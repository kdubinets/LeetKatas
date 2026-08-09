#include <algorithm>
#include <cstddef>
#include <span>

struct Progress {
    std::size_t consumed;
    std::size_t written;
};

Progress solve(std::span<const int> input, std::span<int> output) {
    // Finish: copy one value from each adjacent equal run and report both final positions as counts
}
