# Name

Synchronize with a Latch

# Description

At a supplied one-shot synchronization point, decrement the remaining participant count and block until it reaches zero. This trains the combined arrival-and-wait operation for a latch whose lifetime is managed by the caller.

# Solution

```cpp
ready.arrive_and_wait();
```
