#include <concepts>
#include <iterator>

template <std::input_iterator Iterator>
requires std::constructible_from<std::iter_value_t<Iterator>,
                                 std::iter_rvalue_reference_t<Iterator>>
std::iter_value_t<Iterator> solve(Iterator position) {
    // Finish: construct an owning result through the iterator's move-aware access
}
