#include <type_traits>

int runtime_value() {
    return 2;
}

constexpr int selected_value() {
    // Finish: return 1 during constant evaluation and use the supplied runtime operation otherwise
}

static_assert(selected_value() == 1);
