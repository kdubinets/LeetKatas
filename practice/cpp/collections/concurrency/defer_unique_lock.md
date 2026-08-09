# Name

Defer Lock Acquisition

# Description

Create a movable lock object associated with the supplied mutex without acquiring it immediately, then acquire the mutex before incrementing the caller-owned integer. This isolates deferred acquisition while retaining scope-based release.

# Solution

```cpp
std::unique_lock lock(mutex, std::defer_lock);
lock.lock();
++value;
```
