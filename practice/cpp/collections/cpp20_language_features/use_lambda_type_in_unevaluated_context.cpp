#include <type_traits>

template <class Predicate>
struct Filter {
    Predicate predicate{};
};

using PositiveFilter =
    // Finish: make a filter whose type embeds a directly written captureless positive-number predicate

static_assert(std::is_default_constructible_v<PositiveFilter>);
static_assert(PositiveFilter{}.predicate(1));
static_assert(!PositiveFilter{}.predicate(0));
