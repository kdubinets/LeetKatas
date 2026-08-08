#include <compare>
#include <map>
#include <string>
#include <utility>

struct Key {
    int group;
    int id;
    auto operator<=>(const Key&) const = default;
};

bool solve(std::map<Key, std::string>& values, const Key& old_key, Key new_key) {
    // Finish: replace an existing key without copying its mapped text and report whether it existed
}
