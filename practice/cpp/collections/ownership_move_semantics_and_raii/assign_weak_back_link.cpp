#include <memory>

struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> previous;
};

void solve(const std::shared_ptr<Node>& parent,
           const std::shared_ptr<Node>& child) {
    // Finish: connect parent forward to child and child back to parent without creating a shared-ownership cycle
}
