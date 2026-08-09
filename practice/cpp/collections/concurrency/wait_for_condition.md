# Name

Wait for a Protected Condition

# Description

Wait on the supplied condition variable until the mutex-protected Boolean becomes true. The implementation must recheck the state predicate after wakeups and release the mutex while blocked.

# Solution

```cpp
std::unique_lock lock(mutex);
changed.wait(lock, [&ready] { return ready; });
```
