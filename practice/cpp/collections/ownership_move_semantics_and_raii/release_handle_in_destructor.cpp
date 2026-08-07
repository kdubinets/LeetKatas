void release_handle(int handle) noexcept;

class Handle {
public:
    explicit Handle(int value) : value_(value) {}

    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;

    ~Handle() {
        // Finish: release the handle at scope exit when it is valid
    }

private:
    int value_;
};
