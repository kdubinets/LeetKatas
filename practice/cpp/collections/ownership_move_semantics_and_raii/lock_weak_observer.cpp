#include <memory>

struct Resource {
    int id;
};

std::shared_ptr<Resource> solve(const std::weak_ptr<Resource>& observer) {
    // Finish: return temporary shared ownership when the resource is still alive, or an empty owner otherwise
}
