#include <string>

struct UserKey {
    int organization;
    std::string name;
    int cached_permissions;
};

struct UserKeyEqual {
    bool operator()(const UserKey& left, const UserKey& right) const {
        // Finish: compare exactly the stable identity fields and ignore cached state
    }
};
