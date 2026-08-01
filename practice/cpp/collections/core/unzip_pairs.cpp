#include <string>
#include <utility>
#include <vector>

std::pair<std::vector<int>, std::vector<std::string>> solve(
    const std::vector<std::pair<int, std::string>>& values) {
    std::pair<std::vector<int>, std::vector<std::string>> result;
    result.first.reserve(values.size());
    result.second.reserve(values.size());
    // Finish: preserve input order while placing first fields in the first output and second fields in the second output
    return result;
}
