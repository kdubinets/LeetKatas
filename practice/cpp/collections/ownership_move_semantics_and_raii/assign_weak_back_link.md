# Name

Assign a Weak Back-Link

# Description

Connect two distinct, non-null shared nodes so `parent->next` owns `child` while `child->previous` observes `parent` without owning it. This exercise covers using a weak back-link to avoid a shared-ownership cycle.

# Solution

```cpp
parent->next = child;
child->previous = parent;
```
