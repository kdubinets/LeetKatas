#include <utility>
#include <variant>

enum class Error { invalid, unavailable };
using Result = std::variant<int, Error>;
using Combined = std::variant<std::pair<int, int>, Error>;

Combined solve(const Result& left, const Result& right) {
    // Finish: return both successful integers or the first error from left to right
}
