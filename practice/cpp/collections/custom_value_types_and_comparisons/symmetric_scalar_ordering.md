# Name

Symmetric Scalar Ordering

# Description

Define three-way ordering between a revision value and its integer representation so relational comparisons work with either operand order. Add only the canonical operand order and rely on C++20 rewritten comparison candidates for the reverse direction.

# Solution

```cpp
friend std::strong_ordering operator<=>(Revision revision, int value) {
    return revision.value <=> value;
}
```
