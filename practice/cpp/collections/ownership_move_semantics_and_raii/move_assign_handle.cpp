#include <utility>

void release_handle(int handle) noexcept;

class Handle {
public:
    explicit Handle(int value) : value_(value) {}

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;

    Handle(Handle&& other) noexcept
        : value_(std::exchange(other.value_, -1)) {}

    Handle& operator=(Handle&& other) noexcept {
        // Finish: unless this is self-assignment, release the current valid handle, take the other handle, invalidate the other object, and return this object
    }

    ~Handle() {
        if (value_ != -1) {
            release_handle(value_);
        }
    }

private:
    int value_;
};
