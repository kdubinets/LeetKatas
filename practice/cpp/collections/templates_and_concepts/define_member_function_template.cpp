#include <string>

struct Converter {
    // Finish: define a const member that converts a value to a caller-selected result type
};

int main() {
    const Converter converter;
    return converter.convert<int>(2.5) == 2 &&
                   converter.convert<std::string>("ready") == "ready"
               ? 0
               : 1;
}
