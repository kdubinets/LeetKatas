#include <mutex>
#include <utility>

using namespace std;

template <class Function>
void initialize(std::once_flag& flag, Function&& function) {
    // Finish: invoke the callable through the flag so successful initialization happens only once
}
