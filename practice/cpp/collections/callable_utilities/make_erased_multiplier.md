# Name

Make an Erased Multiplier

# Description

Return a `std::function<int(int)>` that owns the supplied factor and multiplies each integer argument by it. Products are guaranteed representable as `int`. This trains storing a capturing lambda behind a stable, copyable callable signature.

# Solution

```cpp
return [factor](int value) { return value * factor; };
```
