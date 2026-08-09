# Name

Use Scoped Thread Completion

# Description

Start a worker that assigns `42` to caller-owned storage. The worker object must automatically wait for completion when the function scope ends, without an explicit join statement. The caller must keep the referenced integer alive for the call.

# Solution

```cpp
std::jthread worker([&result] { result = 42; });
```
