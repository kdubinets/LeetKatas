# Name

Initialize Nested Aggregate Members

# Description

Return a `Label` with its `position` member initialized by an inner designated initializer for `x` and `y`, and designate `visible` as true. Preserve member declaration order at both levels.

# Solution

```cpp
return Label{.position = {.x = x, .y = y}, .visible = true};
```
