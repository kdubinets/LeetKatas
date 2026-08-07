#include <memory>

struct Resource {
    int id;
};

void solve(std::unique_ptr<Resource>& owner) {
    // Finish: immediately destroy any owned resource and leave the owner empty
}
