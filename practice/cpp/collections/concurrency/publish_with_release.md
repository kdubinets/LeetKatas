# Name

Publish with Release Ordering

# Description

Write an ordinary integer payload, then set the initially false atomic readiness flag with release ordering. This is a one-shot publication: the payload is not modified again after readiness becomes true. A matching acquire observation of `true` must make the preceding payload write visible.

# Solution

```cpp
payload = value;
ready.store(true, std::memory_order_release);
```
