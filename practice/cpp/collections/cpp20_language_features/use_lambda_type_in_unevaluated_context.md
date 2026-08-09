# Name

Use a Lambda Type in an Unevaluated Context

# Description

Define `PositiveFilter` as `Filter` specialized with the closure type of a directly written captureless lambda. The lambda takes an `int` and reports whether it is positive. C++20 permits the lambda expression inside `decltype`, and its closure type can be default-constructed by `Filter`.

# Solution

```cpp
Filter<decltype([](int value) { return value > 0; })>;
```
