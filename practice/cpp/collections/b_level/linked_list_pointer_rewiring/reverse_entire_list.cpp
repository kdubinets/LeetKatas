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

Node* reverse_entire_list(Node* head) {
    // Pattern: iterative three-pointer reversal. The processed nodes form a reversed chain, and the unprocessed suffix remains accessible.

    // Finish: return the head of the same nodes in reverse order, ending in nullptr; return nullptr for empty input
}
