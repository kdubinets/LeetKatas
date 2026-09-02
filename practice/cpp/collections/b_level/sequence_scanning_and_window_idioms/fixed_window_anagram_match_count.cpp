#include <array>
#include <cstddef>
#include <string>

std::size_t count_anagram_windows(const std::string& text, const std::string& pattern) {
    if (pattern.empty() || pattern.size() > text.size()) {
        return 0;
    }

    // Pattern: fixed-size character-frequency window. Keep its frequency state synchronized with the window's entry and exit.
    // Finish: return how many windows are an anagram of pattern; text and pattern contain lowercase English letters
}
