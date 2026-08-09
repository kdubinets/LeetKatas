# Name

Consume a Future Result

# Description

Consume and return the integer from a supplied move-only future, waiting for readiness when necessary. The operation may be performed only once and must also propagate any stored exception to the caller. This trains the consumer side of an asynchronous result handoff.

# Solution

```cpp
return result.get();
```
