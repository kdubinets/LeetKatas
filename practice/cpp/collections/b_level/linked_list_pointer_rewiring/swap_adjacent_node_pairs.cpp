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

Node* swap_adjacent_node_pairs(Node* head) {
    // Pattern: dummy-head pair-block rewiring. The predecessor borders a correctly swapped prefix and the untouched suffix.

    // Finish: return the head with each consecutive pair of original nodes exchanged: A,B,C,D,E becomes B,A,D,C,E; leave an unpaired final node last; end in nullptr and return nullptr for empty input
}
