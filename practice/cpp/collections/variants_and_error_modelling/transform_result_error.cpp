#include <string>
#include <variant>

using namespace std;

enum class Error { invalid, unavailable };
using Input = std::variant<int, Error>;
using Output = std::variant<int, std::string>;

std::string describe(Error);

Output solve(const Input& result) {
    // Finish: preserve a successful integer and convert a failure to descriptive text
}
