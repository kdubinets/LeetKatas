# Name

Construct from an Argument Pack

# Description

Create and return an exclusively owned `T` constructed from the complete argument pack. Preserve each argument's value category when expanding it into construction.

# Solution

```cpp
return std::make_unique<T>(std::forward<Args>(args)...);
```
