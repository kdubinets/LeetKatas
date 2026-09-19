# Name

Swap Adjacent Node Pairs

# Description

Return the head after exchanging each consecutive pair of original nodes. For example, node identities A,B,C,D,E become B,A,D,C,E; exchange nodes, not their stored values. An unpaired final node remains last. The result ends in nullptr, empty input returns nullptr, and a single node remains unchanged. The input is finite and acyclic, and all nodes remain caller-owned. Change links only: do not allocate or delete list nodes or change values. Use constant auxiliary space, including the call stack.

The supplied pattern is dummy-head pair-block rewiring: the predecessor borders a correctly swapped prefix and the untouched suffix. Each completed block must connect to the remaining chain.

This exercise covers repeated two-node block rewiring with a stable prefix boundary.

# Solution

```cpp
Node dummy{0, head};
Node* previous = &dummy;
while (previous->next != nullptr && previous->next->next != nullptr) {
    Node* first = previous->next;
    Node* second = first->next;
    first->next = second->next;
    second->next = first;
    previous->next = second;
    previous = first;
}
return dummy.next;
```
