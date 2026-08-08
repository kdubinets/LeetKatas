#include <string>
#include <type_traits>
#include <variant>

using Value = std::variant<int, std::string>;

std::string solve(const Value& left, const Value& right) {
    // Finish: join the text forms of both active values with a colon between them
}
