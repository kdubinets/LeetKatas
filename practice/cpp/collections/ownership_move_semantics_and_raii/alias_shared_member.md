# Name

Alias a Shared Member

# Description

Given non-null shared ownership of a `Record`, return `std::shared_ptr<const std::string>` pointing at its `name` member while sharing the complete record's lifetime. Do not allocate or copy the string. This exercise covers the aliasing shared-pointer constructor.

# Solution

```cpp
return {owner, &owner->name};
```
