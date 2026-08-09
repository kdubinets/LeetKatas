# Name

Increment an Atomic Counter

# Description

Atomically add one to a supplied integer counter and return its previous value. This trains a single atomic read-modify-write operation rather than a separate load and store.

# Solution

```cpp
return counter.fetch_add(1);
```
