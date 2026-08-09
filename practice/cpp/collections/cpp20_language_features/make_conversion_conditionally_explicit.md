# Name

Make a Conversion Conditionally Explicit

# Description

Define the templated `Value` constructor and initialize `amount` from its argument. Make the constructor implicit exactly for `int` and explicit for other source types using C++20's conditional form of `explicit`.

# Solution

```cpp
explicit(!std::is_same_v<T, int>) Value(T value) : amount(value) {}
```
