#include <memory>
#include <utility>

class Owner {
public:
    explicit Owner(std::unique_ptr<int> value) : value_(std::move(value)) {}

    // Finish: permit ownership transfer but forbid copying

private:
    std::unique_ptr<int> value_;
};
