# Name

Transfer Ownership to a Thread

# Description

Transfer an exclusively owned string into the supplied worker function, let it write the string length to local storage, join the worker, and return the length. This trains move-only thread argument handoff while keeping the result reference valid until completion.

# Solution

```cpp
std::thread worker(consume, std::move(text), std::ref(length));
worker.join();
return length;
```
