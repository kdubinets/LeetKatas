# Name

Merge Two Sorted Node Chains

# Description

Return one null-terminated chain containing every original node from left and right in nondecreasing value order. Preserve node order within each input; for equal values, nodes from left precede nodes from right. Either input may be empty; return nullptr if both are empty. Inputs are disjoint finite acyclic sorted lists, and all nodes remain caller-owned. Links may change, but list nodes must not be allocated or deleted and values must not change. Use constant auxiliary space.

The supplied pattern is a dummy-head tail merge: the output prefix is sorted, its tail borders the unconsumed input chains, and equality selects the left chain.

This exercise covers tail-link maintenance while consuming two disjoint sorted chains.

# Solution

```cpp
Node dummy{0};
Node* tail = &dummy;
while (left != nullptr && right != nullptr) {
    if (left->value <= right->value) {
        tail->next = left;
        left = left->next;
    } else {
        tail->next = right;
        right = right->next;
    }
    tail = tail->next;
}
tail->next = left != nullptr ? left : right;
return dummy.next;
```
