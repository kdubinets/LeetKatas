# Name

Initialize Once

# Description

Invoke a supplied callable through the caller-owned one-time flag, preserving the callable's value category. Across concurrent calls sharing the flag, one successful invocation performs initialization; an exception leaves the flag available for retry.

# Solution

```cpp
std::call_once(flag, std::forward<Function>(function));
```
