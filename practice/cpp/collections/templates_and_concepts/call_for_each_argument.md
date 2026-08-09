# Name

Call for Each Argument

# Description

Invoke the supplied function once for every argument, preserving argument value categories. Calls must occur from left to right, and an empty argument pack must do nothing.

# Solution

```cpp
(static_cast<void>(function(std::forward<Args>(args))), ...);
```
