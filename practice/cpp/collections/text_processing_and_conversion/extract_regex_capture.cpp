#include <cstddef>
#include <optional>
#include <regex>
#include <string>

std::optional<std::string> solve(
    const std::string& text,
    const std::regex& pattern,
    std::size_t group) {
    // Finish: return the requested capture from the first match, with group zero selecting the whole match, or an empty result when it is unavailable or did not participate
}
