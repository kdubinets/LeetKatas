#include <memory>
#include <vector>

struct Resource {
    int id;
};

void solve(std::vector<std::shared_ptr<Resource>>& owners,
           const std::shared_ptr<Resource>& owner) {
    // Finish: append another owner of the same resource so its lifetime is extended by the vector entry
}
