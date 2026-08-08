#include <optional>
#include <string>
#include <utility>
#include <variant>

enum class Error { missing };
using Result = std::variant<std::string, Error>;

Result solve(std::optional<std::string> value) {
    // Finish: return the text when present and an explicit missing error otherwise
}
