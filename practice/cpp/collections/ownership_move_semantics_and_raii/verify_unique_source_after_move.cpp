#include <memory>
#include <utility>

struct Resource {
    int id;
};

bool solve(std::unique_ptr<Resource>& source) {
    // Finish: take the resource into a local owner and report that source became empty while the local owner became nonempty
}
