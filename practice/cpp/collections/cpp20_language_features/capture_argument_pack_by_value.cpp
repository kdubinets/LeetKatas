#include <tuple>
#include <utility>

template <class... Args>
auto defer_values(Args&&... args) {
    // Finish: return a lambda that owns every argument and later returns them as a tuple
}

int main() {
    auto deferred = defer_values(3, 4.5);
    return deferred() == std::tuple{3, 4.5} ? 0 : 1;
}
