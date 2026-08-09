# Name

Read with a Shared Lock

# Description

Return an integer protected by the supplied shared mutex while holding shared, read-only lock ownership. Multiple readers may use this operation concurrently, while writers require exclusive ownership.

# Solution

```cpp
std::shared_lock lock(mutex);
return value;
```
