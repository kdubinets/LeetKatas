# Name

Reverse an Entire Node Chain

# Description

Return the head of the original nodes in reverse order, with the final node's next pointer null. An empty input returns nullptr. The input is a finite acyclic list whose nodes remain caller-owned. Links may change, but list nodes must not be allocated or deleted and values must not change. Use constant auxiliary space.

The supplied pattern is iterative three-pointer reversal: the processed nodes form a reversed chain while the unprocessed suffix remains accessible.

This exercise covers iterative link reversal with preservation of the unprocessed suffix.

# Solution

```cpp
Node* reversed = nullptr;
while (head != nullptr) {
    Node* next = head->next;
    head->next = reversed;
    reversed = head;
    head = next;
}
return reversed;
```
