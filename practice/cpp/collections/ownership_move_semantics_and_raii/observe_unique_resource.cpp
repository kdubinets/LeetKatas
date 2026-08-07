#include <memory>

struct Resource {
    int id;
};

Resource* solve(const std::unique_ptr<Resource>& owner) {
    // Finish: return a nullable pointer for observing the resource without taking ownership
}
