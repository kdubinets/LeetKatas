#include <type_traits>

struct EmptyPolicy {};

struct Storage {
    // Finish: store the empty policy while permitting it to share an address with another member
    int value;
};

static_assert(std::is_empty_v<EmptyPolicy>);

int main() {
    Storage storage{{}, 7};
    return storage.value == 7 ? 0 : 1;
}
