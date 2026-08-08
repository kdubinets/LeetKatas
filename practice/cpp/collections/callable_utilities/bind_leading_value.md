# Name

Bind a Leading Value

# Description

Adapt the provided two-argument function into a `std::function<int(int)>` by storing `base` as its first argument. Calling the result with `value` must compute `value - base`, which is guaranteed representable as `int`.

# Solution

```cpp
return std::bind_front(difference_from, base);
```
