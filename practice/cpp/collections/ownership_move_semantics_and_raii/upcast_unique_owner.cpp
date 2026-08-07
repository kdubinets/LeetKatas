#include <memory>

struct Base {
    explicit Base(int identifier) : id(identifier) {}
    virtual ~Base() = default;

    int id;
};

struct Derived : Base {
    using Base::Base;
};

std::unique_ptr<Base> solve(std::unique_ptr<Derived> owner) {
    // Finish: return ownership of the same object through its base type
}
