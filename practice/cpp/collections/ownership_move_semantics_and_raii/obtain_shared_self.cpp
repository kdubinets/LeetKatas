#include <memory>

using namespace std;

class Node : public std::enable_shared_from_this<Node> {
public:
    std::shared_ptr<Node> owner() {
        // Finish: return an additional shared owner of this node
    }
};
