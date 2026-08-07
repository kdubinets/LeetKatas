#include <memory>
#include <utility>

struct Resource {
    int id;
};

void solve(std::unique_ptr<Resource>& destination,
           std::unique_ptr<Resource>& source) {
    // Finish: transfer source ownership to destination, cleaning up destination's previous resource and leaving source empty
}
