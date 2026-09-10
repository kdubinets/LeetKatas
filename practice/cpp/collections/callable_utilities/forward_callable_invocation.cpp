#include <functional>
#include <utility>

using namespace std;

template <class F, class... Args>
decltype(auto) solve(F&& callable, Args&&... args) {
    // Finish: invoke the callable while preserving all incoming value categories
}
