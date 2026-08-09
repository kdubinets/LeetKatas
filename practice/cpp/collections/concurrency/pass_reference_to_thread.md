# Name

Pass a Reference to a Thread

# Description

Run the supplied increment function on a worker thread so it mutates the caller-owned integer, then wait for the worker. Thread argument storage normally decays and copies arguments, so the implementation must preserve reference semantics explicitly.

# Solution

```cpp
std::thread worker(increment, std::ref(value));
worker.join();
```
