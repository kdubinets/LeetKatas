#include <cstddef>
#include <string>
#include <variant>

enum class Error { invalid, unavailable };
using TextResult = std::variant<std::string, Error>;
using SizeResult = std::variant<std::size_t, Error>;

SizeResult measure_text(const std::string&);

SizeResult solve(const TextResult& result) {
    // Finish: measure successful text while propagating an existing error unchanged
}
