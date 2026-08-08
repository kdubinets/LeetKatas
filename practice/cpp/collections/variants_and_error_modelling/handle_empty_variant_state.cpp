#include <string>
#include <variant>

using Selection = std::variant<std::monostate, int, std::string>;

bool solve(const Selection& selection) {
    // Finish: return whether no selection has been made
}
