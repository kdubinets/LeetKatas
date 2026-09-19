#include <array>
#include <cstddef>
#include <string>

using namespace std;

std::size_t count_anagram_windows(const std::string& text, const std::string& pattern) {
    if (pattern.empty() || pattern.size() > text.size()) {
        return 0;
    }

    // Pattern: fixed-size character-frequency window. Keep its frequency state synchronized with the window's entry and exit.

    // Finish: return the number of substrings of text of length pattern.size() with exactly the same letters and letter counts as pattern; overlapping matches count separately; both strings contain only lowercase English letters
}
