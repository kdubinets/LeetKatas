#include <memory>

struct Base {
    virtual ~Base() = default;
};

struct Derived : Base {
    int value;
};

std::shared_ptr<Derived> solve(const std::shared_ptr<Base>& owner) {
    // Finish: return shared ownership through the derived type when the object has that type, or an empty owner otherwise
}
