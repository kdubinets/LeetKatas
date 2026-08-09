# Name

Notify Atomic Waiters

# Description

Store a new integer state and wake all threads blocked on the supplied atomic object. This trains the publishing side of C++20 atomic wait/notify; waiters still recheck the atomic value themselves.

# Solution

```cpp
state.store(value);
state.notify_all();
```
