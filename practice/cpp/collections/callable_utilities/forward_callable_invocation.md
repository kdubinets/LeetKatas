# Name

Forward a Callable Invocation

# Description

Implement a generic invocation wrapper that accepts any supported callable form and argument list. Forward the callable and every argument, and preserve references in the callable's return type rather than forcing a value copy.

# Solution

```cpp
return std::invoke(
    std::forward<F>(callable),
    std::forward<Args>(args)...);
```
