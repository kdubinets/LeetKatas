# Name

Enable an Integral Overload

# Description

Define `twice` as a function template taking and returning `T`. Place an `std::enable_if_t` constraint in its return type so only integral types produce a viable specialization.

# Solution

```cpp
std::enable_if_t<std::is_integral_v<T>, T> twice(T value) {
    return value + value;
}
```
