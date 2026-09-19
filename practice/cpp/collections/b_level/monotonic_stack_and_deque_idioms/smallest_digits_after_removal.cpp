#include <cstddef>
#include <string>
#include <string_view>

using namespace std;

std::string smallest_digits_after_removal(std::string_view digits, std::size_t remove_count) {
    // Pattern: increasing digit stack with a removal budget. While budget remains, remove larger trailing digits before appending a smaller digit; spend leftover budget from the suffix.

    // Finish: remove exactly remove_count digits while preserving the order of those retained and return the smallest resulting nonnegative decimal representation; digits is nonempty and contains only '0' through '9', remove_count <= digits.size(); omit leading zeroes and return "0" if no nonzero digit remains
}
