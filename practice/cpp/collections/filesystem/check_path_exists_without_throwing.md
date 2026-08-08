# Name

Check Path Existence Without Throwing

# Description

Query whether a path resolves to an existing filesystem object using the non-throwing overload. Return the existence result and place any failure in the caller-provided `std::error_code`, which the caller will inspect before trusting `false`.

# Solution

```cpp
return std::filesystem::exists(value, error);
```
