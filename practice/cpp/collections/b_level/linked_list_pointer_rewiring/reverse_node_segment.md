# Name

Reverse an Indexed Node Segment

# Description

Return the head after reversing the original nodes at zero-based positions first through last, including both endpoints. Every node outside that segment retains its original order, and the result ends in nullptr. Positions refer to the input order, not node values. The input is nonempty, finite, and acyclic, with first <= last < the number of nodes. A one-node segment leaves the chain unchanged; the segment may touch either end or cover the whole chain. All nodes remain caller-owned. Change links only: do not allocate or delete list nodes or change values. Use constant auxiliary space, including the call stack.

The supplied pattern is bounded head-insertion reversal: a fixed predecessor borders the growing reversed segment, while both outside portions retain their original order. Unlike whole-list reversal, this task preserves and reconnects the segment's outer boundaries.

This exercise covers anchored segment reversal with preservation of both outer boundaries.

# Solution

```cpp
Node dummy{0, head};
Node* before = &dummy;
for (std::size_t index = 0; index < first; ++index) {
    before = before->next;
}
Node* segment_tail = before->next;
for (std::size_t moved = 0; moved < last - first; ++moved) {
    Node* node = segment_tail->next;
    segment_tail->next = node->next;
    node->next = before->next;
    before->next = node;
}
return dummy.next;
```
