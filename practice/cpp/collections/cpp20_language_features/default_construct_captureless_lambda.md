# Name

Default-Construct a Captureless Lambda

# Description

Return a value-initialized object of `positive`'s closure type. C++20 makes the closure type of a captureless lambda default-constructible, so do not copy the existing `positive` object.

# Solution

```cpp
return decltype(positive){};
```
