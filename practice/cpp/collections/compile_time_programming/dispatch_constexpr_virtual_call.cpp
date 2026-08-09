class Base {
public:
    virtual constexpr int value() const = 0;
    virtual constexpr ~Base() = default;
};

class Derived final : public Base {
public:
    constexpr explicit Derived(int value) : value_(value) {}

    // Finish: return the stored value when called during constant evaluation

private:
    int value_;
};

consteval int read_polymorphically() {
    Derived derived{42};
    const Base& base = derived;
    return base.value();
}

static_assert(read_polymorphically() == 42);
