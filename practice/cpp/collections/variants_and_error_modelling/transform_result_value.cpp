#include <cstddef>
#include <string>
#include <variant>

enum class Error { invalid, unavailable };
using Input = std::variant<std::string, Error>;
using Output = std::variant<std::size_t, Error>;

Output solve(const Input& result) {
    // Finish: convert successful text to its length while preserving a failure
}
