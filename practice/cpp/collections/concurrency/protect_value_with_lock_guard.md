# Name

Protect a Scoped Mutation

# Description

Increment caller-owned integer state while holding its supplied mutex for the complete operation. This trains fixed-scope mutual exclusion where the lock does not need deferred acquisition or early release.

# Solution

```cpp
std::lock_guard lock(mutex);
++value;
```
