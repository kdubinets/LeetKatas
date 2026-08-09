# Name

Request Jthread Cancellation

# Description

Request cooperative cancellation from a scoped worker, open the supplied latch only after the request, join the worker, and return whether its associated token observed the request. The latch makes the handoff deterministic without sleeps or timing assumptions.

# Solution

```cpp
worker.request_stop();
gate.count_down();
worker.join();
return observed;
```
