#include <cstddef>
#include <string>
#include <string_view>
#include <vector>

using namespace std;

bool word_exists(std::vector<std::string>& grid, std::string_view word) {
    // Pattern: temporary grid marking. After matching a cell, mark it unavailable, explore horizontal and vertical neighbors, and restore it before returning on either success or failure.

    // Finish: return whether word can be formed from any starting cell by horizontal or vertical moves without reusing a cell, restoring grid exactly before returning; grid is rectangular lowercase text, word is lowercase, an empty word returns true, and an empty grid cannot match a nonempty word
}
