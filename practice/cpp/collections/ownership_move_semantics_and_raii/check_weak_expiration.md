# Name

Check Weak Expiration

# Description

Return whether a const `std::weak_ptr<Resource>` no longer has any live shared owner. Do not attempt to access the resource. This exercise covers observing weak-pointer expiration.

# Solution

```cpp
return observer.expired();
```
