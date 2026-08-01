# Name

Sum Tuple with Callable Application

# Description

Return the `long long` sum of three integers stored in a const tuple by invoking one callable with the tuple elements as its arguments. The addition must use `long long` arithmetic. This exercise covers expanding tuple contents into a callable invocation.

# Solution

```cpp
return std::apply([](int a, int b, int c) {
    return static_cast<long long>(a) + b + c;
}, values);
```
