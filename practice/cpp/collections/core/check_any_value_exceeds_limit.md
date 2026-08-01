# Name

Check Any Value Exceeds Limit

# Description

Return whether any integer in a const vector is strictly greater than a supplied limit, leaving the input unchanged. This exercise covers an existential range predicate whose lambda captures external state.

# Solution

```cpp
return std::ranges::any_of(values,
                           [limit](int value) { return value > limit; });
```
