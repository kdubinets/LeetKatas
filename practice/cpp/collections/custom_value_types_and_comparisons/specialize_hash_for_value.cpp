#include <cstddef>
#include <functional>
#include <unordered_set>

struct UserId {
    int value;
    friend bool operator==(const UserId&, const UserId&) = default;
};

// Finish: make the value type usable with the standard default hashing policy

using UserIds = std::unordered_set<UserId>;
