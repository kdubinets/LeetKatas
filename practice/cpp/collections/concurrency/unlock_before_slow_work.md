# Name

Unlock Before Slow Work

# Description

Copy the supplied mutex-protected integer while holding its lock, release the lock explicitly, and then pass the independent copy to the supplied non-throwing operation. This trains using `std::unique_lock` to keep potentially slow work outside a critical section.

# Solution

```cpp
std::unique_lock lock(mutex);
const int snapshot = value;
lock.unlock();
work(snapshot);
```
