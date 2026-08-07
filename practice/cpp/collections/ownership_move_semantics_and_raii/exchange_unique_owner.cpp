#include <memory>
#include <utility>

struct Resource {
    int id;
};

std::unique_ptr<Resource> solve(std::unique_ptr<Resource>& owner) {
    // Finish: return the current exclusive owner and leave owner empty
}
