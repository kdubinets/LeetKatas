#include <memory>

struct Resource {
    explicit Resource(int identifier) : id(identifier) {}
    int id;
};

void solve(std::unique_ptr<Resource>& owner, int id) {
    // Finish: replace the currently owned resource with a newly constructed one having this id
}
