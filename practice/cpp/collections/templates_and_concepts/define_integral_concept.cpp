#include <concepts>

using namespace std;

template <class T>
// Finish: define Integral as the standard requirement for integral types

static_assert(Integral<int>);
static_assert(!Integral<double>);
