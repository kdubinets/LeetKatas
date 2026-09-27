# Flatten a Multilevel Doubly Linked List

Each node of a doubly linked list has `next`, `prev`, and possibly `child`
pointers. A child points to the head of another doubly linked list, which may
itself contain child lists. Flatten the structure into one doubly linked list
using the original nodes. A node's complete child list, including deeper
children in the same order, must appear immediately after that node and before
its original next node. All `child` pointers in the result must be null, and
every `next` and `prev` link must agree with the resulting order.

For example, if the top level is `1 ↔ 2`, node `1` has child list `3 ↔ 4`,
and node `3` has child `5`, the flattened order is `1 ↔ 3 ↔ 5 ↔ 4 ↔ 2`.

Return the head of the flattened list, or null for an empty input. There are
at most 1,000 nodes in total, with values from 1 through `10^5`.
