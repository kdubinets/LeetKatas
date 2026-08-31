#include <charconv>
#include <string_view>

enum class ParseResult {
    success,
    invalid,
    out_of_range,
    trailing_characters,
};

ParseResult solve(std::string_view text) {
    // Finish: return invalid for a non-numeric start, out_of_range for an out-of-range digit sequence even with trailing characters, trailing_characters for other incomplete consumption, or success otherwise
}
