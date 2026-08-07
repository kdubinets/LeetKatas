#include <cstddef>
#include <vector>

class Buffer {
public:
    explicit Buffer(std::size_t size) : data_(size) {}

    std::size_t size() const {
        return data_.size();
    }

private:
    // Finish: store the integers with ordinary value semantics and automatic lifetime management
};
