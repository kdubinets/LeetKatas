# Name

Exchange Atomic State

# Description

Atomically replace a Boolean state with `true` and return the previous state. This covers indivisible replacement and retrieval without a compare-and-exchange condition.

# Solution

```cpp
return active.exchange(true);
```
