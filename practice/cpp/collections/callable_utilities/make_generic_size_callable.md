# Name

Make a Generic Size Callable

# Description

Return a generic lambda that accepts any const object with a `size()` member and returns that member's result. The callable should work for different container and string types without type erasure.

# Solution

```cpp
return [](const auto& value) { return value.size(); };
```
