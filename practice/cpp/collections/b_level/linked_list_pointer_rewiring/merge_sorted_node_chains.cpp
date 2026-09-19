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

Node* merge_sorted_node_chains(Node* left, Node* right) {
    // Pattern: dummy-head tail merge. The output prefix is sorted and its tail borders the unconsumed input chains; prefer left on equality.

    // Finish: return the head of all original nodes from left and right in nondecreasing value order, ending in nullptr; preserve each input's node order and put left nodes before right nodes on equal values; inputs are sorted and disjoint; return nullptr if both are empty
}
