# Name

Require a Compile-Time Condition

# Description

Define `SmallType<T>` with a nested requirement that compares `sizeof(T)` with `sizeof(int)`. Types no larger than `int` must satisfy the concept.

# Solution

```cpp
concept SmallType = requires {
    requires sizeof(T) <= sizeof(int);
};
```
