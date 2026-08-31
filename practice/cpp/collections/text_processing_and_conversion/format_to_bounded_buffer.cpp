#include <algorithm>
#include <cstddef>
#include <format>
#include <iterator>
#include <span>

struct FormatResult {
    std::size_t written;
    std::size_t required;
};

FormatResult solve(std::span<char> output, int value) {
    // Finish: write as much decimal text as fits without a null terminator and report both the written and required character counts
}
