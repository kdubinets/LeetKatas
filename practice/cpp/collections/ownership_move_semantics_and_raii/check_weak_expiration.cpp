#include <memory>

struct Resource {
    int id;
};

bool solve(const std::weak_ptr<Resource>& observer) {
    // Finish: return whether no shared owners of the observed resource remain
}
