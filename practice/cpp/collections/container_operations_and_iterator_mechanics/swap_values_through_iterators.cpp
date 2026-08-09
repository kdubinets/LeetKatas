#include <iterator>

template <class Iterator>
requires std::indirectly_swappable<Iterator, Iterator>
void solve(Iterator left, Iterator right) {
    // Finish: exchange the values referenced by the two iterators
}
