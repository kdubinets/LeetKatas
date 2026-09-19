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

Node* remove_matching_nodes(Node* head, int target) {
    // Pattern: dummy-head predecessor scan. The predecessor stays at the end of the retained prefix when a candidate is excluded.

    // Finish: return the head of all original nodes whose value differs from target, in their original order and ending in nullptr; return nullptr if none remain; excluded nodes' links are unspecified
}
