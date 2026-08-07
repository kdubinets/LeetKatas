#include <cstddef>
#include <ranges>
#include <vector>

using Iterator = std::vector<int>::const_iterator;

std::ranges::subrange<Iterator> solve(const std::vector<int>& values,
                                      std::size_t first,
                                      std::size_t last) {
    // Finish: for valid half-open indices, return a non-owning range between the corresponding iterators
}
