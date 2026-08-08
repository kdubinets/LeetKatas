# Name

Negate a Stored Predicate

# Description

Given a non-empty `std::function<bool(int)>`, return another callable with the same argument type that produces the logical complement of the original predicate. The original wrapper must remain unchanged.

# Solution

```cpp
return std::not_fn(predicate);
```
