# Name

Default Unspecified Aggregate Members

# Description

Return a `Counters` aggregate designating only `pending`. The other members must retain their zero-valued default member initializers.

# Solution

```cpp
return Counters{.pending = pending};
```
