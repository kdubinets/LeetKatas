# Name

Check All Types Match

# Description

Define the initializer for `all_same_as` by testing every type in `Types` against `Expected`. An empty pack must satisfy the condition.

# Solution

```cpp
(std::is_same_v<Expected, Types> && ...);
```
