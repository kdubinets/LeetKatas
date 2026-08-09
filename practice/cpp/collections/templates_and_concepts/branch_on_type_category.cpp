#include <string>
#include <type_traits>

template <class T>
std::string describe(T value) {
    // Finish: return decimal text for integral values and the value itself for other supported types
}

int main() {
    return describe(42) == "42" && describe(std::string{"text"}) == "text" ? 0 : 1;
}
