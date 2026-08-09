// Finish: define an integer cube function whose calls are required to produce compile-time constants

constexpr int value = cube(4);
static_assert(value == 64);
