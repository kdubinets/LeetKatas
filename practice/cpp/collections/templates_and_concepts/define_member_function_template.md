# Name

Define a Member Function Template

# Description

Add a const member function template named `convert` to `Converter`. Its first template parameter is the requested result type, its by-value function argument has an independently deduced type, and it returns the argument explicitly converted to the result type.

# Solution

```cpp
template <class Result, class Source>
Result convert(Source value) const {
    return static_cast<Result>(value);
}
```
