#include <stdexcept>
#include <string>
#include <variant>

using namespace std;

int read_value();

using Result = std::variant<int, std::string>;

Result solve() {
    // Finish: return the read value or the message from a standard failure
}
