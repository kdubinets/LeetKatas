#include <algorithm>
#include <cstddef>
#include <compare>
#include <string>

char ascii_lower(char ch) {
    return ch >= 'A' && ch <= 'Z' ? static_cast<char>(ch + ('a' - 'A')) : ch;
}

struct Label {
    std::string text;

    friend std::weak_ordering operator<=>(const Label& left, const Label& right) {
        // Finish: compare labels lexicographically without ASCII letter case distinguishing them
    }
};
