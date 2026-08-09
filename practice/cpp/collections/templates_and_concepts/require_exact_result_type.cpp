#include <concepts>
#include <cstddef>
#include <string>

struct ApproximateSize {
    int size() const;
};

template <class T>
// Finish: require size on a const value to return exactly std::size_t

static_assert(ExactSize<std::string>);
static_assert(!ExactSize<ApproximateSize>);
