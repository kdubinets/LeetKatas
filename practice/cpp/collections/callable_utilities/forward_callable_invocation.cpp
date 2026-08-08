#include <functional>
#include <utility>

template <class F, class... Args>
decltype(auto) solve(F&& callable, Args&&... args) {
    // Finish: invoke the callable while preserving all incoming value categories
}
