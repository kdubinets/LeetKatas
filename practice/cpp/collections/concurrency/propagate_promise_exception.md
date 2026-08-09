# Name

Propagate an Exception Through a Promise

# Description

Inside the supplied catch-all handler, store the currently handled exception in the promise. A consumer calling `get()` on the associated future must receive the original failure. Successful work is already stored by the surrounding code.

# Solution

```cpp
result.set_exception(std::current_exception());
```
