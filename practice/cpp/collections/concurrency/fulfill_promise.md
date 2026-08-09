# Name

Fulfill a Promise

# Description

Create a promise for an integer, obtain its associated future, store the supplied value in the shared state, and return the future. This isolates successful producer-side result handoff without requiring a worker thread.

# Solution

```cpp
std::promise<int> promise;
auto future = promise.get_future();
promise.set_value(value);
return future;
```
