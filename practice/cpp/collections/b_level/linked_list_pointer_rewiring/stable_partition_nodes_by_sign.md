# Name

Stably Partition Nodes by Sign

# Description

Return a null-terminated chain containing all original nodes, with negative-valued nodes before nonnegative-valued nodes. Preserve original order within each group; zero belongs to the nonnegative group. Empty input returns nullptr. The input is finite and acyclic, and all nodes remain caller-owned. Change links only: do not allocate or delete list nodes or change values. Use constant auxiliary space, including the call stack.

The supplied pattern is two-chain stable partition: each output chain contains its group's processed nodes in original order and ends in nullptr. Joining the groups must not retain stale links into the original order.

This exercise covers two-tail stable partitioning with explicit chain termination.

# Solution

```cpp
Node negative_dummy{0};
Node other_dummy{0};
Node* negative_tail = &negative_dummy;
Node* other_tail = &other_dummy;
while (head != nullptr) {
    Node* next = head->next;
    head->next = nullptr;
    if (head->value < 0) {
        negative_tail->next = head;
        negative_tail = head;
    } else {
        other_tail->next = head;
        other_tail = head;
    }
    head = next;
}
negative_tail->next = other_dummy.next;
return negative_dummy.next;
```
