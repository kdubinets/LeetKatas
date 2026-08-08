#include <cstddef>
#include <functional>
#include <string>

struct UserKey {
    int organization;
    std::string name;
};

struct UserKeyHash {
    std::size_t operator()(const UserKey& key) const {
        // Finish: produce a hash that incorporates both identity fields
    }
};
