#include <string>

std::string combine(std::string first) {
    return first;
}

std::string combine(std::string first, std::string second) {
    return first + second;
}

// Finish: define COMBINE so it passes an optional second argument without leaving a comma when absent

int main() {
    return COMBINE("a") == "a" && COMBINE("a", "b") == "ab" ? 0 : 1;
}
