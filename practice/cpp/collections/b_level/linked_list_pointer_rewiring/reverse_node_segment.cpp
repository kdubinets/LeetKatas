#include <cstddef>

using namespace std;

struct Node {
    int value;
    Node* next = nullptr;
};

/*
Nodes remain caller-owned. Input chains are finite, acyclic, and end in nullptr.
Change links only: do not allocate or delete list nodes or change values.
Use constant auxiliary space, including the call stack.
*/

Node* reverse_node_segment(Node* head, std::size_t first, std::size_t last) {
    // Pattern: bounded head-insertion reversal. A fixed predecessor borders the growing reversed segment; both outside portions retain their original order.

    // Finish: return the head after reversing original nodes at zero-based positions first through last, inclusive, while keeping every other node in its original order; end in nullptr; head is nonempty and first <= last < the number of nodes
}
