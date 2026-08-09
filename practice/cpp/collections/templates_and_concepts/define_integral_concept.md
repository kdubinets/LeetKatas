# Name

Define an Integral Concept

# Description

Define the named concept `Integral<T>` so it is satisfied exactly when the standard integral concept accepts `T`.

# Solution

```cpp
concept Integral = std::integral<T>;
```
