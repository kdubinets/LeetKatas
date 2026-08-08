#include <algorithm>
#include <cstddef>
#include <string_view>

char ascii_lower(char ch) {
    return ch >= 'A' && ch <= 'Z' ? static_cast<char>(ch + ('a' - 'A')) : ch;
}

struct CaseInsensitiveEqual {
    bool operator()(std::string_view left, std::string_view right) const {
        return std::ranges::equal(left, right, {}, ascii_lower, ascii_lower);
    }
};

struct CaseInsensitiveHash {
    std::size_t operator()(std::string_view text) const {
        // Finish: hash text consistently with the supplied ASCII case-insensitive equality
    }
};
