#include <memory>
#include <utility>

struct Resource {
    int id;
};

std::shared_ptr<Resource> solve(std::unique_ptr<Resource> owner) {
    // Finish: transfer the exclusively owned resource into shared ownership
}
