# Name

Initialize an Aggregate by Member

# Description

Return an `Options` aggregate using C++20 member designators to set `verbose` to true and `timeout` to 30. Retain the default for `retries` and list designated members in declaration order.

# Solution

```cpp
return Options{.verbose = true, .timeout = 30};
```
