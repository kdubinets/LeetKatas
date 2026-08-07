#include <utility>

void release_handle(int handle) noexcept;

class Handle {
public:
    explicit Handle(int value) : value_(value) {}

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;

    Handle(Handle&& other) noexcept
        // Finish: initialize this object with the other handle and mark the other object invalid

    ~Handle() {
        if (value_ != -1) {
            release_handle(value_);
        }
    }

private:
    int value_;
};
