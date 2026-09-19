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

Node* stable_partition_nodes_by_sign(Node* head) {
    // Pattern: two-chain stable partition. Each output chain contains its group's processed nodes in original order and ends in nullptr.

    // Finish: return the head of all original nodes with negative values before nodes with nonnegative values, preserving original order within each group and ending in nullptr; return nullptr for empty input
}
