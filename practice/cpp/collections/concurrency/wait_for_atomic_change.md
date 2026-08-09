# Name

Wait for an Atomic Change

# Description

Block efficiently while the supplied atomic integer still equals an already observed value, then return its current value. This covers C++20 atomic waiting without a sleep or hand-written polling loop.

# Solution

```cpp
state.wait(observed);
return state.load();
```
