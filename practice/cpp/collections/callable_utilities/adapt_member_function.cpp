#include <functional>

struct Scale {
    int factor;

    int apply(int value) const {
        return factor * value;
    }
};

std::function<int(const Scale&, int)> solve() {
    // Finish: return a regular callable that applies Scale's operation to an object and integer
}
