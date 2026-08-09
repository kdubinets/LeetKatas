# Name

Wait with Cancellation

# Description

Wait on the supplied general condition variable until protected readiness becomes true or the stop token is requested. Return true only when the predicate was satisfied. This covers C++20 stop-aware predicate waiting.

# Solution

```cpp
std::unique_lock lock(mutex);
return changed.wait(lock, token, [&ready] { return ready; });
```
