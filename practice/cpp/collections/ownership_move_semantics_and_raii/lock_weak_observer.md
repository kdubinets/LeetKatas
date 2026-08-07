# Name

Lock a Weak Observer

# Description

Given a const `std::weak_ptr<Resource>`, return shared ownership if the resource still exists or an empty `std::shared_ptr<Resource>` if it has expired. This exercise covers safely promoting a non-owning observation before access.

# Solution

```cpp
return observer.lock();
```
