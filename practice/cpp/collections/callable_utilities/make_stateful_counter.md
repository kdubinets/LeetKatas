# Name

Make a Stateful Counter

# Description

Return a `std::function<int()>` that owns mutable counter state. Successive calls must return `first`, `first + 1`, and so on, independently of the local parameter after `solve` returns. The caller limits calls so every returned value remains representable as `int`.

# Solution

```cpp
return [current = first]() mutable { return current++; };
```
