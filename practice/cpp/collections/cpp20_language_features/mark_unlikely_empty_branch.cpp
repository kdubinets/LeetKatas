#include <string_view>

std::size_t checked_length(std::string_view text) {
    // Finish: treat empty input as an uncommon zero-result branch and otherwise return the length
}

int main() {
    return checked_length("") == 0 && checked_length("abc") == 3 ? 0 : 1;
}
