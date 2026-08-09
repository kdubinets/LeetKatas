# Name

Launch an Asynchronous Task

# Description

Invoke the supplied integer function through `std::async` with an explicit policy that requires asynchronous execution, forwarding the integer argument and returning the result future. The task must not be eligible for deferred execution.

# Solution

```cpp
return std::async(std::launch::async, work, value);
```
