# Name

Consume with Acquire Ordering

# Description

Load the atomic readiness flag with acquire ordering. Return absence when it is false; after observing true, return the ordinary integer payload from a one-shot publisher that used a release operation and will not modify the payload again. This isolates the consuming half of a release/acquire handoff without spinning.

# Solution

```cpp
if (!ready.load(std::memory_order_acquire)) {
    return std::nullopt;
}
return payload;
```
