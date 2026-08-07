#include <charconv>
#include <string_view>

enum class ParseResult {
    success,
    invalid,
    out_of_range,
    trailing_characters,
};

ParseResult solve(std::string_view text) {
    // Finish: classify the complete decimal integer input into the appropriate result category
}
