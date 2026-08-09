#include <memory>
#include <string>
#include <utility>

template <class T, class... Args>
std::unique_ptr<T> create(Args&&... args) {
    // Finish: create T from all arguments while preserving their value categories
}

int main() {
    auto value = create<std::string>(4, 'x');
    return *value == "xxxx" ? 0 : 1;
}
