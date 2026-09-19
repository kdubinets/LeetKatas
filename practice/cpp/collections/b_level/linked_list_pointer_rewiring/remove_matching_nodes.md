# Name

Remove All Matching Nodes

# Description

Return the head of all original nodes whose value differs from target, in their original order, with the final retained node's next pointer null. Return nullptr for empty input or if all nodes are excluded. The input is a finite acyclic list whose nodes remain caller-owned, including excluded nodes. Links on excluded nodes are unspecified. Links may change, but list nodes must not be allocated or deleted and values must not change. Use constant auxiliary space.

The supplied pattern is a dummy-head predecessor scan: the predecessor remains at the end of the retained prefix when a candidate is excluded, including consecutive matching nodes.

This exercise covers predecessor-link maintenance during repeated node exclusion.

# Solution

```cpp
Node dummy{0, head};
Node* previous = &dummy;
while (previous->next != nullptr) {
    Node* candidate = previous->next;
    if (candidate->value == target) {
        previous->next = candidate->next;
    } else {
        previous = candidate;
    }
}
return dummy.next;
```
