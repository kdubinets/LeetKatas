# Name

Bind a Member to an Object Reference

# Description

Return a `std::function<int(int)>` that calls `Accumulator::add` on the supplied existing object. The callable must keep referring to that object rather than storing an independent copy of it. Supplied additions are guaranteed not to overflow `int`.

# Solution

```cpp
return std::bind_front(&Accumulator::add, std::ref(accumulator));
```
